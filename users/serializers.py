from django.contrib.auth import get_user_model
from rest_framework import serializers

from courses.models import Course


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Список всех пользователей"""
    url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('public_id', 'username', 'avatar', 'url')

    def get_url(self, obj):
        return obj.get_absolute_url()  # используем метод модели


class CourseMiniSerializer(serializers.ModelSerializer):
    """Вложенный сериализатор для курсов"""

    class Meta:
        model = Course
        fields = ("public_id", "title")


class UserSerializerRetrieve(serializers.ModelSerializer):
    """Просмотр чужого профиля """
    authored_courses = CourseMiniSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'public_id', 'username', 'first_name', 'last_name',
            'avatar', 'authored_courses'
        )


class MeSerializerRetrieve(serializers.ModelSerializer):
    """Детальный просмотр своего профиля """

    email = serializers.EmailField(read_only=True)  # делаем поле недатированным
    username = serializers.EmailField(read_only=True)  # делаем поле недатированным

    studying_courses = serializers.SerializerMethodField()  # список курсов, на которых учится пользователь
    folders = serializers.SerializerMethodField()  # список папок пользователя
    authored_courses = serializers.SerializerMethodField()  # список курсов, созданных пользователем
    followers = serializers.SerializerMethodField()  # список пользователей, подписанных на текущего
    following = serializers.SerializerMethodField()  # список пользователей, на которых подписан текущий

    class Meta:
        model = User
        fields = (
            'public_id', 'username', 'first_name', 'last_name',
            'avatar', 'email', 'studying_courses', 'folders',
            'followers', 'following', 'authored_courses',
        )

    def get_studying_courses(self, obj):
        """Список изучаемых курсов"""
        return list(obj.studying_courses.values_list('course__title', flat=True))

    def get_folders(self, obj):
        """Список папок пользователя"""
        return list(obj.folders.values_list('title', flat=True))

    def get_authored_courses(self, obj):
        """Возвращает список курсов, которые создал пользователь"""
        return list(obj.authored_courses.values_list('title', flat=True))

    def get_followers(self, obj):
        """Возвращает список пользователей, которые подписаны на текущего пользователя"""
        return list(obj.followers.values_list('username', flat=True))

    def get_following(self, obj):
        """ Возвращает список пользователей, на которых подписан текущий пользователь"""
        return list(obj.following.values_list('username', flat=True))



