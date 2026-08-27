import pytest
from users.models import User, Follow

pytestmark = pytest.mark.django_db  # разрешаем использовать базу данных


class TestUserModel:
    """Тестирование пользовательской модели User"""

    data_user = {
        "username": "test_user",
        "email": "test@gmail.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "test_password"
    }
    data_superuser = {
        "username": "test_superuser",
        "email": "testsuperuser@gmail.com",
        "first_name": "Test",
        "last_name": "Superuser",
        "password": "test_password"
    }

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.user = User.objects.create_user(**self.data_user)
        self.admin = User.objects.create_superuser(**self.data_superuser)

    def test_create_user(self):
        """Проверка успешного создания пользователя"""
        assert self.user.username == self.data_user["username"]
        assert self.user.email == self.data_user["email"]
        assert self.user.first_name == self.data_user["first_name"]
        assert self.user.last_name == self.data_user["last_name"]
        assert self.user.is_active is True
        assert not self.user.is_staff
        assert not self.user.is_superuser
        assert self.user.check_password("test_password")

    def test_create_superuser(self):
        """Проверка создания суперпользователя"""
        assert self.admin.username == self.data_superuser["username"]
        assert self.admin.email == self.data_superuser["email"]
        assert self.admin.first_name == self.data_superuser["first_name"]
        assert self.admin.last_name == self.data_superuser["last_name"]
        assert self.admin.is_superuser
        assert self.admin.is_staff
        assert self.admin.check_password(self.data_superuser["password"])

    def test_create_user_without_email_raises_error(self):
        """Ошибка при отсутствии email"""
        with pytest.raises(TypeError):
            User.objects.create_user(username="no_email", email=None, password="12345")

    def test_str_representation(self):
        """Проверка строкового представления"""
        assert str(self.user) == f"{self.user.username} {self.user.last_name}"

    def test_user_uuid_auto_created(self):
        """UUID должен генерироваться автоматически"""
        assert self.user.public_id is not None

    def test_ordering_by_created(self):
        """Проверка сортировки пользователей по дате создания"""
        # Создаем еще одного пользователя для проверки сортировки
        another_user = User.objects.create_user(
            username="another_user",
            email="another@gmail.com",
            password="another_pass"
        )
        users = list(User.objects.all())
        assert users[0].created >= users[-1].created


class TestFollowModel:
    """Тестирование промежуточной модели Follow"""

    data_user = {
        "username": "test_user",
        "email": "test@gmail.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "test_password"
    }

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.first_user = User.objects.create_user(**self.data_user)
        self.second_user = User.objects.create_user(
            username="another_user",
            email="another@gmail.com",
            password="another_pass"
        )
        self.follow = Follow.objects.create(user_from=self.first_user, user_to=self.second_user)

    def test_create_follow(self):
        """Проверка успешного создания подписки"""
        assert self.follow.user_from == self.first_user
        assert self.follow.user_to == self.second_user
        assert str(self.follow) == f"{self.first_user} подписался на {self.second_user}"

    def test_unique_constraint(self):
        """Нельзя подписаться на одного пользователя дважды"""
        with pytest.raises(Exception):
            Follow.objects.create(user_from=self.first_user, user_to=self.second_user)

    def test_cascade_delete(self):
        """При удалении пользователя должны удаляться его подписки"""
        # Создаем дополнительную подписку для проверки
        third_user = User.objects.create_user(
            username="third_user",
            email="third@gmail.com",
            password="third_pass"
        )
        Follow.objects.create(user_from=self.first_user, user_to=third_user)

        # Удаляем пользователя и проверяем, что его подписки удалились
        follow_count_before = Follow.objects.count()
        self.first_user.delete()
        follow_count_after = Follow.objects.count()

        # Все подписки, где first_user был user_from, должны удалиться
        assert follow_count_after == follow_count_before - 2
