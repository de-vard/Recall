import datetime

from flashcards.models import FlashCardSet
from study.models import StudySession, CardProgress
from mongo_snapshot import MongoSnapshotService

mongo = MongoSnapshotService()  # сервис MongoDB


class SessionStudy:
    def __init__(self, user_id, flashcard_set_id):
        self.user_id = user_id
        self.flashcard_set_id = flashcard_set_id
        self.session = StudySession.objects.get_or_create(
            user=self.user_id, flashcard_set=self.flashcard_set_id)[0]

    def get_cards(self):
        """Карточки которые в наборе-изучения"""
        return FlashCardSet.objects.get(public_id=self.flashcard_set_id).cards.all()

    def get_cardprogress(self, card):
        """Возвращает прогресс по КОНКРЕТНОЙ карточки"""
        return CardProgress.objects.get_or_create(
            user=self.user_id,
            card=card
        )[0]


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
        self.session.end_time = datetime.datetime.now()
        self.session.cards_studied = self.cards_studied
        self.session.cards_known = self.cards_known
        self.session.save()
        mongo.save_snapshot_studysession(self.session)
