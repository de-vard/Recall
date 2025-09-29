import uuid
from django.db import models

class Folder(models.Model):
    """Для папок"""
    public_id = models.UUIDField(
        db_index=True,  # Ускоряет поиск по public_id.
        unique=True,  # Запрещает дубликаты.
        default=uuid.uuid4,  # Автоматически генерирует UUID.
        editable=False,  # Нельзя изменить вручную.
    )
    title = models.CharField(verbose_name="Название", max_length=255)
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="+", # отключаем атрибут для экономии системных ресурсов
        verbose_name="Создатель папки"
    )
    parent_folder = models.ForeignKey(
        'self', # Создаем рекурсивную связь, для связи таблицы на себя, для возможности создавать вложеные папки
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name="Папка родитель",
        blank=True,
        null=True
    )
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    class Meta:
        # Добовляем ограничение что бы, у одного владельца в одной родительской папке не было папок с одинаковым названием
        unique_together = ('owner', 'parent_folder', 'title')