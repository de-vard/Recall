from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import BooleanField

from flashcards.models import FlashCardSet, Card

User = get_user_model()


class CardProgress(models.Model):
    """Прогресс изучения КОНКРЕТНОЙ карточки пользователем"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Изучающий")
    card = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name="Изучающая карточка")
    is_known = models.BooleanField(verbose_name="Знает/Не знает термин?", default=False)
    date_answer = models.DateTimeField(verbose_name="Дата ответа", auto_now=True, )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'card'], name='unique_user_card')
        ]
        verbose_name = "Прогресс карточки"
        verbose_name_plural = "Прогресс карточек"

    def knows_word(self) -> BooleanField:
        """Возвращает True, если пользователь знает слово"""
        return self.is_known


class StudySession(models.Model):
    """Хранение изученных наборов карточек"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь изучающий карточки")
    flashcard_set = models.ForeignKey(FlashCardSet, on_delete=models.CASCADE, verbose_name="Набор карточек")
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="Начало сессии")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Окончание сессии")
    cards_studied = models.IntegerField(default=0, verbose_name="Количество изучаемых карточек")
    cards_known = models.IntegerField(default=0, verbose_name="Количество изученных слов за сессию")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'flashcard_set'], name='unique_user_flashcard_set')
        ]
        verbose_name = "Сессия изучения"
        verbose_name_plural = "Сессии изучения"
