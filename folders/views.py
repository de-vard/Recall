from rest_framework import generics
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from folders.models import Folder
from folders.permissions import IsAuthor
from folders.serializers import FolderSerializer, FolderCreateSerializer


class FolderRootView(APIView):
    """Получить домашнюю папку пользователя."""
    permission_classes = [IsAuthor]

    def get(self, request):
        try:
            folder = Folder.objects.prefetch_related("children", "courses").get(
                owner=request.user,
                title="home"
            )
        except Folder.DoesNotExist:
            raise NotFound("Home folder not found")

        return Response(FolderSerializer(folder).data)


class FolderAPIRetrieve(generics.RetrieveDestroyAPIView):
    """Отображение содержимого папки и ее удаление"""
    queryset = Folder.objects.all().prefetch_related("children", "courses")
    permission_classes = [IsAuthor]
    serializer_class = FolderSerializer
    lookup_field = 'public_id'

    def destroy(self, request, *args, **kwargs):
        """Проверка, что папка не пустая перед удалением """
        folder = self.get_object()

        # Проверяем, есть ли внутри папки, которую удаляем курсы или папки
        has_children = folder.children.exists()
        has_courses = folder.courses.exists()

        if has_children or has_courses:
            raise ValidationError("Нельзя удалить папку: она не пустая.")

        if folder.title == "home":
            raise ValidationError("Не удаляйте корневую папку пожалуйста")

        return super().destroy(request, *args, **kwargs)


class FolderAPICreate(generics.CreateAPIView):
    """Создание папки"""
    queryset = Folder.objects.all()
    serializer_class = FolderCreateSerializer

    @staticmethod
    def _check_title(parent_folder, title):
        """
        Проверяем, существует ли папка с таким же названием внутри parent_folder.
        Если существует — добавляем -1, -2, -3 и т.д. пока не получим уникальное имя.
        """

        # Получаем список всех названий дочерних папок внутри parent_folder.
        # values_list(..., flat=True) возвращает простой список строк, а не список кортежей.
        # Оборачиваем в set, чтобы поиск "in" был быстрее (O(1)).
        existing_titles = set(
            parent_folder.children.values_list("title", flat=True)
        )

        counter = 1
        original_title = title  # сохраняем оригинальное название

        # Пока текущее название уже существует — добавляем суффикс "-1", "-2", ...
        while title in existing_titles:
            title = f"{original_title}-{counter}"
            counter += 1

        return title

    def perform_create(self, serializer):
        # Достаём public_id родительской папки из URL
        parent_public_id = self.kwargs.get("public_id")

        # Проверяем, существует ли такая папка и принадлежит ли она текущему пользователю
        try:
            parent_folder = Folder.objects.get(public_id=parent_public_id, owner=self.request.user)
        except Folder.DoesNotExist:
            # Если папка не найдена — поднимаем ошибку
            raise ValidationError("Parent folder not found")

        # Проверяем уникальность имени в рамках родительской папки
        new_title = self._check_title(parent_folder, serializer.validated_data["title"])

        # Сохраняем новую папку, явно указывая родителя и владельца
        serializer.save(
            owner=self.request.user,
            parent_folder=parent_folder,
            title=new_title
        )


class FolderAPIUpdate(generics.UpdateAPIView):
    """Редактирование папки"""
    queryset = Folder.objects.all()
    serializer_class = FolderCreateSerializer
    permission_classes = [IsAuthor]
    lookup_field = "public_id"

    def update(self, request, *args, **kwargs):
        """Проверка, что пользователь не изменяет папку home"""
        folder = self.get_object()
        if folder.title == "home":
            raise ValidationError("Не изменяйте название корневой папки пожалуйста")
        return super().update(request, *args, **kwargs)

    @staticmethod
    def _check_title(parent_folder, title, current_public_id):
        """
        Проверяем уникальность title внутри родительской папки.
        Исключаем текущую папку по public_id (PK модели).
        """

        existing_titles = set(
            parent_folder.children
            .exclude(public_id=current_public_id)
            .values_list("title", flat=True)
        )

        counter = 1
        base_title = title

        while title in existing_titles:
            title = f"{base_title}-{counter}"
            counter += 1

        return title

    def perform_update(self, serializer):
        folder_instance = self.get_object()  # текущая редактируемая папка
        parent_folder = folder_instance.parent_folder

        # Получаем новое название
        new_title = serializer.validated_data.get("title", folder_instance.title)

        # Генерируем уникальное имя
        new_title = self._check_title(
            parent_folder,
            new_title,
            folder_instance.public_id  # <-- ВАЖНО
        )

        serializer.save(title=new_title)
