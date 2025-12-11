from django.db import models
from rest_framework.reverse import reverse

from backend_apps.abstract.models import AbstractModel, ProxyModel
from backend_apps.courses.models import Course
from backend_apps.media.models import Sound, Image


class FlashCardSet(AbstractModel, ProxyModel):
    """Набор карточек"""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курсы'
    )

    def get_absolute_url(self):
        return reverse('flashcards-detail', kwargs={'public_id': self.public_id})

    class Meta:
        verbose_name = "Набор"
        verbose_name_plural = "Наборы"
        ordering = ["-created"]


class Card(AbstractModel):
    """Карточка"""
    title = None  # Удаляем поле которое наследуется из AbstractModel

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
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Фото'
    )
    sound = models.ForeignKey(
        Sound,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Аудиофайл'
    )

    def get_absolute_url(self):
        return reverse('card-detail', kwargs={'public_id': self.public_id})

    def __str__(self):
        return f"{self.term} - {self.definition}"

    class Meta:
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"
        ordering = ["-created"]
