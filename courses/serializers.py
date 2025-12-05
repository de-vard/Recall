from django.contrib.auth import get_user_model
from rest_framework import serializers

from courses.models import Course
from flashcards.models import FlashCardSet

User = get_user_model()


class CourseListSerializer(serializers.ModelSerializer):
    """Список курсов"""
    students_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    author = serializers.CharField(source='author.username')

    class Meta:
        model = Course
        fields = ('title', 'description', 'author', 'students_count', 'likes_count', 'url')

    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_students_count(self, obj):
        """Количество студентов"""
        return obj.students_count

    def get_likes_count(self, obj):
        """Количество лайков """
        return obj.likes_count


class CourseRetrieveSerializer(serializers.ModelSerializer):
    """Детальный просмотр курса когда на него не подписан"""
    students_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    author = serializers.CharField(source='author.username')

    class Meta:
        model = Course
        fields = (
            'title', 'description', 'author',
            'students_count', 'likes_count', 'url',
        )

    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_students_count(self, obj):
        """Количество студентов"""
        return obj.students_count

    def get_likes_count(self, obj):
        """Количество лайков """
        return obj.likes_count


class UserShortSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('url', 'username')

    def get_url(self, obj):
        return obj.get_absolute_url()


class LessonShortSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = FlashCardSet
        fields = ('url', 'title')

    def get_url(self, obj):
        return obj.get_absolute_url()


class CourseCreate(serializers.ModelSerializer):
    """Создание курса"""
    class Meta:
        model = Course
        fields = ('title', 'description', 'is_public')
        read_only_fields = ("public_id", "author", "folder")


class CourseDetailSerializer(serializers.ModelSerializer):
    """Детальный просмотр курса если пользователь подписан на курс"""
    students_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    students = UserShortSerializer(many=True, read_only=True)
    likes = UserShortSerializer(many=True, read_only=True)
    lessons = LessonShortSerializer(many=True, read_only=True)
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Course
        fields = (
            'title', 'description', 'author',
            'students_count', 'likes_count', 'url',
            'lessons', 'students', 'likes'
        )

    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_students_count(self, obj):
        """Количество студентов"""
        return obj.students_count

    def get_likes_count(self, obj):
        """Количество лайков """
        return obj.likes_count
