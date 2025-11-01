import mimetypes

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import FileField
from django.utils.deconstruct import deconstructible

from mutagen import File as MutagenFile

from abstract.models import AbstractModel, ProxyModel


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


class SoundField(FileField):
    """Поле для хранения аудиофайлов с проверкой через Mutagen"""

    description = "Поле для хранения звуковых файлов"

    def __init__(self, *args, **kwargs):
        # Добавляем свои валидаторы
        validators = kwargs.pop("validators", [])
        validators.append(self.validate_audio_file)
        validators.append(self.validate_audio_file_use_mutagen)
        super().__init__(validators=validators, *args, **kwargs)

    @staticmethod
    def validate_audio_file(value):
        """Проверка по MIME-типу (по расширению файла)"""
        mime_type, _ = mimetypes.guess_type(value.name)
        if not mime_type or not mime_type.startswith("audio"):
            raise ValidationError("Файл должен быть аудио (mp3, wav, ogg и т.д.)")

    @staticmethod
    def validate_audio_file_use_mutagen(value):
        """ Глубокая проверка через Mutagen (анализ содержимого
            файла, что он действительно аудио, а не другой файл с расширением аудио)
        """
        try:
            audio = MutagenFile(getattr(value, "file", value))
            if audio is None or not hasattr(audio, "info"):
                raise ValidationError("Файл не является поддерживаемым аудиофайлом.")
        except Exception:
            raise ValidationError("Файл повреждён или не читается как аудио.")


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


class Sound(AbstractModel, ProxyModel):
    """Модель для хранения звука"""

    uploaded_by_user = models.ForeignKey(
        'users.User',
        verbose_name="Кто загрузил файл",
        on_delete=models.CASCADE,
        related_name="+",  # отключаем атрибут для экономии системных ресурсов
    )
    path_file = SoundField(verbose_name="Ссылка на файл", upload_to="files/sounds/%Y/%m/%d")
