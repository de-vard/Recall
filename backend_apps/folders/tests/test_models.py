from uuid import uuid4

import pytest
from django.http import Http404
from django.db.utils import IntegrityError

from backend_apps.users.models import User
from backend_apps.folders.models import Folder


pytestmark = pytest.mark.django_db


class TestAbstractManager:
    """Тестирование методов менеджера AbstractManager"""

    def test_get_object_by_public_id_success(self, user):
        """Проверка, что менеджер возвращает объект по public_id"""
        folder = Folder.objects.create(title="Test", owner=user)
        found = Folder.objects.get_object_by_public_id(folder.public_id)
        assert found == folder
        assert found.title == "Test"

    def test_get_object_by_public_id_not_found(self):
        """Проверка, что при неправильном ID возвращается Http404"""
        invalid_id = uuid4()
        result = Folder.objects.get_object_by_public_id(invalid_id)
        assert result == Http404


class TestFolderModel:
    """Тестирование модели Folder"""

    def test_create_folder(self, user):
        """Создание папки пользователем"""
        folder = Folder.objects.create(title="Work", owner=user)
        assert folder.title == "Work"
        assert folder.owner == user
        assert folder.parent_folder is None

    def test_str_method(self, user):
        """Проверяем строковое представление модели"""
        folder = Folder.objects.create(title="Projects", owner=user)
        assert str(folder) == f"{folder.title}"

    def test_unique_together_constraint(self, user):
        """Проверяем ограничение unique_together (нельзя создать дубликат папки)"""
        parent = Folder.objects.create(title="Parent", owner=user)
        Folder.objects.create(title="Child", owner=user, parent_folder=parent)

        with pytest.raises(IntegrityError):
            Folder.objects.create(title="Child", owner=user, parent_folder=parent)

    def test_nested_folder_creation(self, user):
        """Проверяем создание вложенных папок"""
        root = Folder.objects.create(title="Root", owner=user)
        subfolder = Folder.objects.create(title="Sub", owner=user, parent_folder=root)

        assert subfolder.parent_folder == root
        assert subfolder.title == "Sub"


class TestUserSignal:
    """Проверяем, что сигнал post_save создаёт корневую папку пользователю"""

    def test_post_save_creates_root_folder(self, db):
        """При создании пользователя автоматически создаётся корневая папка"""
        user = User.objects.create_user(
            username="sig_user",
            email="sig@test.com",
            password="12345"
        )

        folder = Folder.objects.filter(owner=user, title="home", parent_folder=None).first()

        assert folder is not None
        assert folder.title == "home"
        assert folder.owner == user
        assert folder.parent_folder is None
