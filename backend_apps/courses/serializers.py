from django.contrib.auth import get_user_model
from rest_framework import serializers

from backend_apps.courses.models import Course
from backend_apps.flashcards.models import FlashCardSet

User = get_user_model()


class UserShortSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("url", "username")

    def get_url(self, obj):
        return obj.get_absolute_url()


class LessonShortSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = FlashCardSet
        fields = ("url", "title")

    def get_url(self, obj):
        return obj.get_absolute_url()


class BaseCourseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор"""
    url = serializers.SerializerMethodField()
    author = serializers.CharField(source="author.username", read_only=True)
    students_count = serializers.IntegerField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = (
            "title", "description", "author",
            "students_count", "likes_count", "url",
        )

    def get_url(self, obj):
        return obj.get_absolute_url()


class CourseListSerializer(BaseCourseSerializer):
    """Список курсов — только базовые поля"""
    pass


class CourseDetailSerializer(BaseCourseSerializer):
    """Детальный просмотр — добавляем связанные поля"""
    students = UserShortSerializer(many=True, read_only=True)
    likes = UserShortSerializer(many=True, read_only=True)
    lessons = LessonShortSerializer(many=True, read_only=True)

    class Meta(BaseCourseSerializer.Meta):
        fields = BaseCourseSerializer.Meta.fields + (
            "lessons",
            "students",
            "likes",
        )


class CourseCreate(serializers.ModelSerializer):
    """Создание курса"""

    class Meta:
        model = Course
        fields = ("title", "description", "is_public", "folder")
        read_only_fields = ("public_id", "author")
