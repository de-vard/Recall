from rest_framework import serializers

from backend_apps.courses.models import Course
from backend_apps.folders.models import Folder


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
    courses = CourseShortSerializer(many=True, read_only=True)  # делаем поле недатированным
    parent_folder = serializers.PrimaryKeyRelatedField(read_only=True)  # делаем поле недатированным
    parent_title = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ('public_id', 'title', 'parent_folder', 'parent_title', 'children', 'courses')

    def get_parent_title(self, obj):
        """Получаем заголовок родительской папки"""
        if obj.parent_folder:
            return obj.parent_folder.title
        return None


class FolderCreateSerializer(serializers.ModelSerializer):
    # Поле для передачи родительской папки через UUID при создании новой папки
    # write_only=True значит, что клиент отправляет это поле, но оно не возвращается в ответе
    parent_public_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Folder
        fields = ("title", "parent_public_id")

    def validate_parent_public_id(self, value):
        """Метод для валидации конкретного поля parent_public_id"""

        request = self.context["request"]
        try:
            # Пытаемся найти родительскую папку с указанным UUID, принадлежащую текущему пользователю
            return Folder.objects.get(owner=request.user, public_id=value)
        except Folder.DoesNotExist:
            # Если папка не найдена — вызываем ValidationError
            raise serializers.ValidationError("Родительская папка не найдена")

    def validate(self, attrs):
        """Метод для валидации всего объекта целиком"""
        request = self.context["request"]
        parent = attrs["parent_public_id"]  # здесь уже объект Folder после validate_parent_public_id
        title = attrs["title"]  # название новой папки

        # Проверяем, есть ли уже папка с таким названием у этого пользователя и в этой родительской папке
        if Folder.objects.filter(owner=request.user, parent_folder=parent, title=title).exists():
            # Если есть — выбрасываем ValidationError, возвращаем ошибку по ключу "title"
            raise serializers.ValidationError({"title": "Папка с таким названием уже существует в этой директории"})
        return attrs  # Если все проверки пройдены, возвращаем attrs для дальнейшего использования в create()

    def create(self, validated_data):
        """Метод создания новой папки после успешной валидации"""
        # Извлекаем объект родительской папки, который пришел через validated_data
        parent_folder = validated_data.pop("parent_public_id")
        return Folder.objects.create(owner=self.context["request"].user, parent_folder=parent_folder, **validated_data)


class FolderUpdateSerializer(serializers.ModelSerializer):
    """Редактирование папки """

    class Meta:
        model = Folder
        fields = ("title",)

    def validate_title(self, value):
        folder = self.instance  # текущая папка, которую обновляем
        parent = folder.parent_folder
        owner = folder.owner

        # Проверяем, есть ли другая папка с таким же title у того же пользователя и родителя
        if Folder.objects.filter(owner=owner, parent_folder=parent, title=value).exclude(pk=folder.pk).exists():
            raise serializers.ValidationError("Папка с таким названием уже существует в этой директории")
        return value
