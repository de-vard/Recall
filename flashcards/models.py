from django.db import models

from abstract.models import AbstractModel, ProxyModel
from courses.models import Course
from media.models import Sound, Image


class FlashCardSet(AbstractModel, ProxyModel):
    """Набор карточек"""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курсы'
    )


class CardQuerySet(models.QuerySet):
    """QuerySet оптимизирующий загрузку связанных данных"""
    def optimized(self):
        """Добавляем в QuerySet свой метод"""
        return self.select_related("image", "sound")


class CardManager(models.Manager):
    """Менеджер, использующий оптимизированный QuerySet"""
    def get_queryset(self):
        """Используем свой QuerySet вызывая метод оптимизации"""
        return CardQuerySet(self.model, using=self._db).optimized()


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

    objects = CardManager()

    def __str__(self):
        return f"{self.term} - {self.definition}"
