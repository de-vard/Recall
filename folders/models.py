from django.db import models
from django.urls import reverse

from abstract.models import AbstractModel


class Folder(AbstractModel):
    """Модель для папок"""

    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="folders",  # отключаем атрибут для экономии системных ресурсов
        verbose_name="Создатель папки"
    )
    parent_folder = models.ForeignKey(
        'self',  # Создаем рекурсивную связь, для связи таблицы на себя, для возможности создавать вложенные папки
        on_delete=models.PROTECT,
        related_name="children",
        verbose_name="Папка родитель",
        blank=True,
        null=True,

    )

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('folder-home', kwargs={'public_id': self.public_id})

    class Meta:
        verbose_name = "Папка"
        verbose_name_plural = "Папки"
        # Добавляем ограничение, что бы, у одного владельца в одной родительской
        # папке не было папок с одинаковым названием
        unique_together = ('owner', 'parent_folder', 'title')
