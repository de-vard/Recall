from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend_apps.folders.models import Folder
from backend_apps.folders.permissions import IsAuthor
from backend_apps.folders.serializers import FolderSerializer, FolderCreateSerializer


class FolderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthor]
    lookup_field = "public_id"
    lookup_url_kwarg = "public_id"

    def get_queryset(self):
        """Фильтруем папки только для текущего пользователя"""
        return Folder.objects.filter(owner=self.request.user).prefetch_related("children", "courses")

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return FolderCreateSerializer
        return FolderSerializer

    def list(self, request, *args, **kwargs):
        """Возвращает домашнюю папку пользователя с ее содержимым"""
        try:
            folder = Folder.objects.prefetch_related("children", "courses").get(
                owner=request.user,
                title="home"
            )
        except Folder.DoesNotExist:
            raise NotFound("Home folder not found")

        return Response(FolderSerializer(folder).data)

    def destroy(self, request, *args, **kwargs):
        """Проверка, что папка не пустая перед удалением."""
        folder = self.get_object()

        if folder.children.exists() or folder.courses.exists():
            raise ValidationError("Нельзя удалить папку: она не пустая.")

        if folder.title == "home":
            raise ValidationError("Не удаляйте корневую папку пожалуйста")

        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Определяем UUID родителя, если не указан, то тогда указываем home, также проверяем что имя уникальное"""
        parent_public_id = self.kwargs.get("public_id")
        if parent_public_id:
            parent_folder = Folder.objects.get(public_id=parent_public_id, owner=self.request.user)
        else:
            parent_folder = Folder.objects.get(owner=self.request.user, title="home")

        new_title = self.request.data.get("title")
        self._validate_unique_title(parent_folder, new_title)

        serializer.save(owner=self.request.user, parent_folder=parent_folder)

    def update(self, request, *args, **kwargs):
        """Защита от переименования корневой папки"""
        folder = self.get_object()
        new_title = request.data.get("title")

        if folder.title == "home":
            raise ValidationError("Не изменяйте название корневой папки пожалуйста")

        self._validate_unique_title(folder.parent_folder, new_title, exclude_public_id=folder.public_id)

        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def create_child(self, request, public_id=None):
        """Возможно создавать папки внутри других папок"""
        parent_folder = self.get_object()

        new_title = request.data.get("title")
        self._validate_unique_title(parent_folder, new_title)

        folder = Folder.objects.create(
            title=new_title,
            owner=request.user,
            parent_folder=parent_folder
        )
        return Response(FolderSerializer(folder).data, status=201)

    @staticmethod
    def _validate_unique_title(parent_folder, new_title, exclude_public_id=None):
        """Проверка на уникальность имени"""
        if not new_title:
            return

        qs = parent_folder.children.all()

        if exclude_public_id:
            qs = qs.exclude(public_id=exclude_public_id)

        if qs.filter(title=new_title).exists():
            raise ValidationError(f"Папка с названием '{new_title}' уже существует в этой директории")
