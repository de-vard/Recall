import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.deconstruct import deconstructible


@deconstructible
class SizeValueValidator:
    """Кастомный валидатор размера файла (в мегабайтах)"""

    def __init__(self, max_size_mb=5):
        self.max_size_mb = max_size_mb

    def __call__(self, file):
        """Проверяет размер файла"""
        size_mb = file.size / (1024 * 1024)  # переводим в МБ
        if size_mb > self.max_size_mb:
            raise ValidationError(
                f"Размер файла {size_mb:.2f} МБ превышает допустимый лимит {self.max_size_mb} МБ.",
                code="invalid"
            )


class Image(models.Model):
    """Модель для хранения изображения"""
    public_id = models.UUIDField(
        db_index=True,  # Ускоряет поиск по public_id.
        unique=True,  # Запрещает дубликаты.
        default=uuid.uuid4,  # Автоматически генерирует UUID.
        editable=False,  # Нельзя изменить вручную.
    )
    title = models.CharField(verbose_name="Название", max_length=255)
    image_file = models.ImageField(
        verbose_name="Ссылка на файл",
        upload_to="images/%Y/%m/%d",
        validators=[
            SizeValueValidator(max_size_mb=3)  # созданный кастомный валидатор для проверки размера файла
        ],
    )
    uploaded_by_user = models.ForeignKey(
        'users.User',
        verbose_name="Кто загрузил изображение",
        on_delete=models.CASCADE,
        related_name="+",  # отключаем атрибут для экономии системных ресурсов
    )
    created = models.DateTimeField(verbose_name="Дата загрузки", auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
