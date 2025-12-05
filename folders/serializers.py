from rest_framework import serializers

from courses.models import Course
from folders.models import Folder


class FolderChildSerializer(serializers.ModelSerializer):
    """Сериализатор для дочерних папок"""
    url = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ('url', 'public_id', 'title',)

    def get_url(self, obj):
        return obj.get_absolute_url()


class CourseShortSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для курсов в папке"""
    url = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'url', 'public_id', 'title',
        )
        ref_name = 'FolderCourseShort'  # Уникальное имя

    def get_url(self, obj):
        return obj.get_absolute_url()


class FolderSerializer(serializers.ModelSerializer):
    """Получение папки и ее содержимое"""
    children = FolderChildSerializer(many=True, read_only=True)  # делаем поле недатированным
    parent_folder = serializers.PrimaryKeyRelatedField(read_only=True)  # делаем поле недатированным
    courses = CourseShortSerializer(many=True, read_only=True)  # делаем поле недатированным
    go_back = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ('public_id', 'title', 'parent_folder', 'go_back', 'children', 'courses')

    def get_go_back(self, obj):
        """Вернуться на одну директорию назад"""
        if obj.parent_folder:
            return obj.parent_folder.public_id
        return obj.public_id


class FolderCreateSerializer(serializers.ModelSerializer):
    """Создание папки """

    class Meta:
        model = Folder
        fields = ("public_id", "title", "parent_folder")
        read_only_fields = ("public_id", "parent_folder")
