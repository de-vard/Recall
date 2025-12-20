from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend_apps.folders.models import Folder
from backend_apps.folders.permissions import IsAuthor
from backend_apps.folders.serializers import FolderSerializer, FolderCreateSerializer, FolderUpdateSerializer


class FolderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthor]
    lookup_field = "public_id"
    lookup_url_kwarg = "public_id"

    def get_queryset(self):
        """Фильтруем папки только для текущего пользователя"""
        return Folder.objects.filter(owner=self.request.user).prefetch_related("children", "courses")

    def get_serializer_class(self):
        if self.action == "create":
            return FolderCreateSerializer
        if self.action in ("update", "partial_update"):
            return FolderUpdateSerializer
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

    def update(self, request, *args, **kwargs):
        """Защита от переименования корневой папки"""
        folder = self.get_object()
        if folder.title == "home":
            raise ValidationError("Не изменяйте название корневой папки, пожалуйста")
        return super().update(request, *args, **kwargs)
