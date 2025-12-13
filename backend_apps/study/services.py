from django.utils import timezone

from django.contrib.auth import get_user_model

from backend_apps.flashcards.models import FlashCardSet
from backend_apps.study.models import StudySession, CardProgress
from backend_apps.study.mongo_snapshot import MongoSnapshotService

mongo = MongoSnapshotService()  # сервис MongoDB

User = get_user_model()


class SessionStudy:
    def __init__(self, user_id, flashcard_set_id):
        self.user = User.objects.get(public_id=user_id)
        self.flashcard_set = FlashCardSet.objects.get(public_id=flashcard_set_id)

        self.session = StudySession.objects.get_or_create(
            user=self.user,
            flashcard_set=self.flashcard_set
        )[0]

    def get_cards(self):
        """Карточки которые в наборе-изучения"""
        return self.flashcard_set.cards.all()

    def get_cardprogress(self, card):
        """Возвращает прогресс по КОНКРЕТНОЙ карточки"""
        return CardProgress.objects.get_or_create(
            user=self.user,
            card=card,
            session=self.session
        )[0]

    def delete_session(self):
        """Удаление сессии"""
        self.session.delete()


class StudyService(SessionStudy):
    """Класс для вывода слов для обучения"""

    def __init__(self, user_id, flashcard_set_id):
        super().__init__(user_id, flashcard_set_id)
        self.cards_studied = 0
        self.cards_known = 0

    def get_cards_when_is_unknown(self):
        """Карточки которые не изучены пользователем"""
        cards = []
        for card in self.get_cards():
            if not self.get_cardprogress(card).is_known:  # если пользователь не знает слово, добавляем в список
                cards.append(card)
        return cards

    def save_result_cards(self, cards: dict):
        """Сохраняем результат карточек"""
        self.cards_studied = len(cards)
        for card, is_known in cards.items():
            progress = self.get_cardprogress(card)
            progress.is_known = is_known
            if is_known:
                self.cards_known += 1
            progress.save()
            mongo.save_snapshot_cardprogress(progress)

    def save_result_session(self):
        self.session.end_time = timezone.now()
        self.session.cards_studied = self.cards_studied
        self.session.cards_known = self.cards_known
        self.session.save()
        mongo.save_snapshot_studysession(self.session)

    def delete_session(self):
        """Удаление сессии и карточек связанных с ней, а также истории изучения(карточек и сессии) в MongoBD"""
        mongo.delete_cardprogress(  # удаляем результаты слов из mongo
            self.user.public_id,
            self.session.id
        )
        mongo.delete_studysession(  # удаляем результаты сессии из mongo
            self.user.public_id,
            self.flashcard_set.public_id
        )
        super().delete_session()

    def get_cardprogress_history(self, card_id):
        """История изучения карточки"""
        return mongo.get_cardprogress_history(self.user.public_id, card_id)

    def get_studysession_history(self):
        """История сессии"""
        return mongo.get_studysession_history(self.user.public_id, self.flashcard_set.public_id)
