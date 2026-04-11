from django.contrib.auth import get_user_model
from rest_framework import serializers
from django_redis import get_redis_connection
from django.utils import timezone
from datetime import timedelta
from backend_apps.courses.models import Course
from backend_apps.users.models import Follow

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Список всех пользователей"""
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return obj.get_absolute_url()  # используем метод из модели

    class Meta:
        model = User
        fields = ('public_id', 'username', 'avatar', 'url', 'user_type')


class CourseMiniSerializer(serializers.ModelSerializer):
    """Вложенный сериализатор для курсов"""

    class Meta:
        model = Course
        fields = ("public_id", "title")


class UserSerializerRetrieve(serializers.ModelSerializer):
    """Просмотр чужого профиля """
    authored_courses = CourseMiniSerializer(many=True, read_only=True)
    is_online = serializers.SerializerMethodField()
    last_active = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    count_followers = serializers.SerializerMethodField()  # количество пользователей, подписанных на текущего
    count_following = serializers.SerializerMethodField()  # количество пользователей, на которых подписан текущий

    class Meta:
        model = User
        fields = (
            'public_id', 'username', 'first_name', 'last_name',
            'avatar', 'is_online', 'last_active', 'user_type', 'bio',
            'count_followers', 'count_following', 'authored_courses',
            'is_following',
        )

    def get_is_following(self, obj):
        """Проверяет, подписан ли текущий пользователь на этого человека"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        # Проверяем через промежуточную модель Follow
        return Follow.objects.filter(
            user_from=request.user,
            user_to=obj
        ).exists()

    def get_is_online(self, obj):
        """
        Проверяет, считается ли пользователь онлайн прямо сейчас.

        Логика:
        1. Берём текущее соединение с Redis
        2. Получаем score (время последнего захода) пользователя из sorted set "online_users"
        3. Если записи нет → пользователь точно не онлайн
        4. Если запись есть → сравниваем его время с порогом (сейчас минус 10 минут)
           Если время последнего действия ≥ порога → считаем онлайн
        """
        # Подключаемся к Redis (используем пул соединений из настроек django-redis)
        r = get_redis_connection("default")

        # ID пользователя должен быть строкой — Redis работает со строковыми ключами
        user_id = str(obj.public_id)

        # Получаем score (Unix timestamp последнего захода) для этого пользователя
        # Если пользователя нет в множестве → вернёт None
        score = r.zscore("online_users", user_id)

        # Нет записи → пользователь не онлайн
        if score is None:
            return False

        # Вычисляем пороговое время: сейчас минус 10 минут
        # Всё, что новее этого времени — считается "онлайн"
        threshold = timezone.now() - timedelta(minutes=10)

        # Сравниваем: был ли пользователь активен после порогового времени
        # score — это число (секунды с 1970), сравниваем с int(threshold.timestamp())
        return score >= int(threshold.timestamp())

    def get_last_active(self, obj):
        """
        Возвращает точное время последней активности пользователя (datetime объект).

        Используется для отображения:
        • "был 5 минут назад"
        • "онлайн"
        • или просто даты/времени, если давно не заходил

        Возвращает None, если пользователь никогда не был замечен в "online_users"
        """
        # То же подключение к Redis
        r = get_redis_connection("default")

        user_id = str(obj.public_id)

        # Получаем timestamp последнего захода
        score = r.zscore("online_users", user_id)

        # Нет данных → возвращаем None (в шаблоне/фронте можно показать "давно не был")
        if score is None:
            return None

        # Преобразуем Unix timestamp (float) обратно в объект datetime
        # с учётом часового пояса проекта (настроенного в settings TIME_ZONE)
        last_time = timezone.datetime.fromtimestamp(
            score,
            tz=timezone.get_current_timezone()
        )

        # Возвращаем готовый datetime объект
        # Дальше можно форматировать на фронте или в сериализаторе:
        # "5 минут назад", "вчера в 14:30", "онлайн" и т.д.
        return last_time

    def get_count_followers(self, obj):
        # Todo: код не оптимизированный, добавил как заглушку, перейду на метод Count вы будущем
        """Возвращает количество пользователей, которые подписаны на текущего пользователя"""
        return len(list(obj.followers.values_list('username', flat=True)))

    def get_count_following(self, obj):
        # Todo: код не оптимизированный, добавил как заглушку, перейду на метод Count вы будущем
        """ Возвращает количество пользователей, на которых подписан текущий пользователь"""
        return len(list(obj.following.values_list('username', flat=True)))


class MeSerializerRetrieve(serializers.ModelSerializer):
    """Детальный просмотр своего профиля """
    # Todo: От наследуйся от UserSerializerRetrieve, что бы не было повтора кода

    email = serializers.EmailField(read_only=True)  # делаем поле не редактированным
    username = serializers.EmailField(read_only=True)  # делаем поле не редактированным

    studying_courses = serializers.SerializerMethodField()  # список курсов, на которых учится пользователь
    folders = serializers.SerializerMethodField()  # список папок пользователя
    authored_courses = serializers.SerializerMethodField()  # список курсов, созданных пользователем
    followers = serializers.SerializerMethodField()  # список пользователей, подписанных на текущего
    following = serializers.SerializerMethodField()  # список пользователей, на которых подписан текущий
    count_followers = serializers.SerializerMethodField()  # количество пользователей, подписанных на текущего
    count_following = serializers.SerializerMethodField()  # количество пользователей, на которых подписан текущий

    class Meta:
        model = User
        fields = (
            'public_id', 'username', 'first_name', 'last_name',
            'avatar', 'email', 'studying_courses', 'folders',
            'followers', 'following', 'authored_courses', 'user_type',
            'bio', 'count_followers', 'count_following',
        )

    def get_studying_courses(self, obj):
        """Список изучаемых курсов"""
        return list(obj.studying_courses.values_list('course__title', flat=True))

    def get_folders(self, obj):
        """Список папок пользователя"""
        return list(obj.folders.values_list('title', flat=True))

    def get_authored_courses(self, obj):
        """Возвращает список курсов с public_id и title"""
        return CourseMiniSerializer(
            obj.authored_courses.all(),
            many=True
        ).data

    def get_followers(self, obj):
        """Возвращает список пользователей, которые подписаны на текущего пользователя"""
        return list(obj.followers.values_list('username', flat=True))

    def get_following(self, obj):
        """ Возвращает список пользователей, на которых подписан текущий пользователь"""
        return list(obj.following.values_list('username', flat=True))

    def get_count_followers(self, obj):
        # Todo: код не оптимизированный, добавил как заглушку, перейду на метод Count вы будущем
        """Возвращает количество пользователей, которые подписаны на текущего пользователя"""
        return len(list(obj.followers.values_list('username', flat=True)))

    def get_count_following(self, obj):
        # Todo: код не оптимизированный, добавил как заглушку, перейду на метод Count вы будущем
        """ Возвращает количество пользователей, на которых подписан текущий пользователь"""
        return len(list(obj.following.values_list('username', flat=True)))


class UserAuthSerializer(serializers.ModelSerializer):
    """Минимальная информация о пользователе при логине. Для авторизации"""

    class Meta:
        model = User
        fields = ("public_id", "username", "email", "avatar", "user_type")
