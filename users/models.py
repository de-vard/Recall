import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from abstract.models import AbstractManager
from media.models import SizeValueValidator


class UserManager(BaseUserManager, AbstractManager):
    """Менеджер модели"""

    def _create_user(self, username, email, password=None, **kwargs):
        """Используем приватный метод, для создания пользователя, что бы не повторять код"""
        if password is None:
            raise TypeError('Users must have a password.')
        if email is None:
            raise TypeError('Users must have an email.')
        if username is None:
            raise TypeError('Users must have a username.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **kwargs):
        """Создаёт и возвращает обычного пользователя"""
        user = self._create_user(username, email, password, **kwargs)
        # TODO: разработать активацию подтверждения пользователя по email, ниже код закомментирован временно так как
        #  реализация подтверждения будет создана позже,поэтому для удобства пока пользователи создаются активными
        # user.is_active = False
        # user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **kwargs):
        """Создаёт и возвращает суперпользователя"""
        user = self._create_user(username, email, password, **kwargs)
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
    first_name = models.CharField(verbose_name="Имя", max_length=255)
    last_name = models.CharField(verbose_name="Фамилия", max_length=255)
    email = models.EmailField(verbose_name="email", db_index=True, unique=True)

    is_staff = models.BooleanField(verbose_name="Персонал?", default=False)  # необходим для админки
    is_active = models.BooleanField(verbose_name="Активная УЗ", default=True)
    is_superuser = models.BooleanField(verbose_name="Суперпользователь?", default=False)

    updated = models.DateTimeField(verbose_name="Обновление данных", auto_now=True, )
    created = models.DateTimeField(verbose_name="Дата регистрации", auto_now_add=True, )

    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/%d",
        validators=[SizeValueValidator(max_size_mb=3)],  # созданный кастомный валидатор для проверки размера файла
        blank=True,
        null=True
    )

    following = models.ManyToManyField(
        'self',  # Указываем рекурсивную связь
        through='Follow',  # указываем использовать промежуточную модель
        symmetrical=False,  # Делаем связь несимметричной. При подписке на пользователя он не подписывается на вас
        # автоматически, то есть (если я подписался на вас, это не значит, что вы подписались на меня).

        related_name='followers',  # Даёт доступ к "обратной стороне" то есть user.following.all() → список
        # пользователей, на которых я подписан. user.followers.all() → список пользователей, которые подписаны на меня.
    )

    USERNAME_FIELD = 'email'  # Явно указываем поле, используемое для аутентификации
    EMAIL_FIELD = 'email'  # Явно указываем поле для email
    REQUIRED_FIELDS = ['username']  # обязательные при создании через createsuperuser

    objects = UserManager()  # Указываем менеджер модели

    def __str__(self):
        return f"{self.username} {self.last_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-created"]


class Follow(models.Model):
    """Промежуточная модель подписки на пользователя"""
    user_from = models.ForeignKey(
        'users.User',
        verbose_name="Подписавшийся пользователь",
        related_name='+',  # тут мы не только экономим ресурсы, но также и решаем проблему с тем одинаковыми названиями
        on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        'users.User',
        verbose_name="Пользователь, на кого подписались",
        related_name='+',  # тут мы не только экономим ресурсы, но также и решаем проблему с тем одинаковыми названиями
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['-created']), ]
        ordering = ['-created']
        unique_together = ('user_from', 'user_to')  # запрещаем дублирующиеся подписки

        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def __str__(self):
        return f'{self.user_from} подписался на {self.user_to}'
