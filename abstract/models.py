from django.db import models
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class AbstractManager(models.Manager):
    """Базовый менеджер модели"""

    def get_object_by_public_id(self, public_id):
        """Метод для поиска по public_id"""
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404


class AbstractModel(models.Model):
    """Базовый абстрактный класс модели"""
    public_id = models.UUIDField(
        primary_key=True,
        db_index=True,  # Ускоряет поиск по public_id.
        unique=True,  # Запрещает дубликаты.
        default=uuid.uuid4,  # Автоматически генерирует UUID.
        editable=False,  # Нельзя изменить вручную.
    )
    title = models.CharField(verbose_name="Название", max_length=255)
    updated = models.DateTimeField(verbose_name="Обновление данных", auto_now=True, )
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True, )

    objects = AbstractManager()

    class Meta:
        abstract = True
