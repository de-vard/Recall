import pytest
from users.models import User


@pytest.fixture
def user():
    """Создание тестового пользователя"""
    data_user = {
        "username": "test_user",
        "email": "test@gmail.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "test_password"
    }

    return User.objects.create_user(**data_user)
