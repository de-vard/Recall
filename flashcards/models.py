import uuid

from django.db import models

from abstract.models import AbstractModel, AbstractManager
from courses.models import Course
from media.models import Sound, Image


class FlashCardSet(AbstractModel):
    """Набор карточек"""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курсы'
    )


class Card(models.Model):
    """Карточка"""
    public_id = models.UUIDField(
        db_index=True,  # Ускоряет поиск по public_id.
        unique=True,  # Запрещает дубликаты.
        default=uuid.uuid4,  # Автоматически генерирует UUID.
        editable=False,  # Нельзя изменить вручную.
    )
    term = models.TextField(verbose_name="Термин")
    definition = models.TextField(verbose_name="Определения")
    transcription = models.TextField(verbose_name="Транскрипция", blank=True, null=True)
    flashcard = models.ForeignKey(
        FlashCardSet,
        on_delete=models.CASCADE,
        related_name='cards',
        verbose_name='Набор карточек'
    )
    image = models.ForeignKey(
        Image,
        # TODO: При удалении изображения в карточках пропадет оно тоже, как насчет запрета на удаление ?
        on_delete=models.CASCADE,

        null=True,
        blank=True,
        verbose_name='Фото'
    )
    sound = models.ForeignKey(
        Sound,
        # TODO: При удалении аудио  в карточках пропадет оно тоже, как насчет запрета на удаление ?
        on_delete=models.CASCADE,

        null=True,
        blank=True,
        verbose_name='Аудиофайл'
    )

    objects = AbstractManager()
