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
    """Отображение содержимого папки"""
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

        return super().destroy(request, *args, **kwargs)


class FolderAPICreate(generics.CreateAPIView):
    """Создание папки"""
    queryset = Folder.objects.all()
    serializer_class = FolderCreateSerializer

