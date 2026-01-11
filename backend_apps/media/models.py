import mimetypes

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import FileField
from django.utils.deconstruct import deconstructible

from mutagen import File as MutagenFile

from backend_apps.abstract.models import AbstractModel, ProxyModel


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


def validate_audio_file_mime(value):
    """Проверка по MIME-типу"""
    mime_type, _ = mimetypes.guess_type(value.name)
    if not mime_type or not mime_type.startswith("audio"):
        raise ValidationError("Файл должен быть аудио (mp3, wav, ogg и т.д.)")


def validate_audio_file_mutagen(value):
    """Проверка через Mutagen"""
    try:
        audio = MutagenFile(getattr(value, "file", value))
        if audio is None or not hasattr(audio, "info"):
            raise ValidationError("Файл не является поддерживаемым аудиофайлом.")
    except Exception:
        raise ValidationError("Файл повреждён или не читается как аудио.")


class SoundField(FileField):
    """Поле для хранения аудиофайлов с проверкой через Mutagen"""

    description = "Поле для хранения звуковых файлов"

    def __init__(self, *args, **kwargs):
        # Добавляем свои валидаторы
        validators = kwargs.pop("validators", [])
        validators.extend([validate_audio_file_mime, validate_audio_file_mutagen])
        kwargs['validators'] = validators
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Удаляем валидаторы из kwargs, чтобы они не участвовали в сериализации
        # Они будут добавлены при инициализации
        kwargs.pop('validators', None)
        return name, path, args, kwargs


class Image(AbstractModel, ProxyModel):
    """Модель для хранения изображения"""

    uploaded_by_user = models.ForeignKey(
        'users.User',
        verbose_name="Кто загрузил файл",
        on_delete=models.CASCADE,
        related_name="+",  # отключаем атрибут для экономии системных ресурсов
    )
    path_file = models.ImageField(
        verbose_name="Ссылка на файл",
        upload_to="files/images/%Y/%m/%d",
        validators=[
            SizeValueValidator(max_size_mb=3)  # созданный кастомный валидатор для проверки размера файла
        ],
    )

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
        ordering = ["-created"]


class Sound(AbstractModel, ProxyModel):
    """Модель для хранения звука"""

    uploaded_by_user = models.ForeignKey(
        'users.User',
        verbose_name="Кто загрузил файл",
        on_delete=models.CASCADE,
        related_name="+",  # отключаем атрибут для экономии системных ресурсов
    )
    path_file = SoundField(verbose_name="Ссылка на файл", upload_to="files/sounds/%Y/%m/%d")

    class Meta:
        verbose_name = "Произношение"
        verbose_name_plural = "Произношения"
        ordering = ["-created"]
