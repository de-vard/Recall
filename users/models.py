import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from media.models import Image


class UserManager(BaseUserManager):
    """Менеджер модели"""

    def get_object_by_public_id(self, public_id):
        """Метод для поиска по public_id"""
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404

    def create_user(self, username, email, password=None, **kwargs):
        """Создаёт и возвращает обычного пользователя"""
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')
        if password is None:
            raise TypeError('User must have a password.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **kwargs):
        """Создаёт и возвращает суперпользователя"""
        if password is None:
            raise TypeError('Superusers must have a password.')
        if email is None:
            raise TypeError('Superusers must have an email.')
        if username is None:
            raise TypeError('Superusers must have a username.')

        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Пользовательская модель"""
    public_id = models.UUIDField(
        db_index=True,  # Ускоряет поиск по public_id.
        unique=True,  # Запрещает дубликаты.
        default=uuid.uuid4,  # Автоматически генерирует UUID.
        editable=False,  # Нельзя изменить вручную.
    )
    username = models.CharField(verbose_name="Логин пользователя", db_index=True, unique=True, max_length=255)
    first_name = models.CharField(verbose_name="Имя",  max_length=255)
    last_name = models.CharField(verbose_name="Фамилия", max_length=255)
    email = models.EmailField(verbose_name="email", db_index=True, unique=True)

    is_staff = models.BooleanField(verbose_name="Персонал?", default=False)  # необходим для админки
    is_active = models.BooleanField(verbose_name="Активная УЗ", default=True)
    is_superuser = models.BooleanField(verbose_name="Суперпользователь?", default=False)

    image_avatar = models.ForeignKey(
        Image,
        verbose_name="Изображдение аватарки",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+", # отключаем атрибут для экономии системных ресурсов
    )
    updated = models.DateTimeField(verbose_name="Обновление данных",auto_now=True)
    created = models.DateTimeField(verbose_name="Дата регистрации",auto_now_add=True)

    USERNAME_FIELD = 'email'  # поле, используемое для аутентификации
    REQUIRED_FIELDS = ['username']  # обязательные при создании через createsuperuser
    objects = UserManager()

