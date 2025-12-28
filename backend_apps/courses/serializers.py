from django.contrib.auth import get_user_model
from rest_framework import serializers

from backend_apps.courses.models import Course, CourseLike, CourseStudent
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
    class Meta:
        model = FlashCardSet
        fields = ("public_id", "title")


class BaseCourseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор"""
    author = serializers.CharField(source="author.username", read_only=True)
    students_count = serializers.IntegerField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    folder_title = serializers.CharField(source="folder.title", read_only=True)

    class Meta:
        model = Course
        fields = (
            "title", "description", "author",
            "students_count", "likes_count",
            "folder", "folder_title", "public_id"
        )


class CourseDetailSerializer(BaseCourseSerializer):
    """Детальный просмотр — добавляем связанные поля"""
    students = UserShortSerializer(many=True, read_only=True)
    likes = UserShortSerializer(many=True, read_only=True)
    lessons = LessonShortSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta(BaseCourseSerializer.Meta):
        fields = BaseCourseSerializer.Meta.fields + (
            "lessons", "students", "likes", "is_liked", "is_subscribed",
        )

    def get_is_liked(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return CourseLike.objects.filter(user=user, course=obj).exists()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return CourseStudent.objects.filter(user=user, course=obj).exists()


class CourseCreate(serializers.ModelSerializer):
    """Создание курса"""

    class Meta:
        model = Course
        fields = ("title", "description", "is_public", "folder")
        read_only_fields = ("public_id", "author")
