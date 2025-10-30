from study.models import StudySession, CardProgress
from mongo_snapshot import MongoSnapshotService

mongo = MongoSnapshotService()  # сервис MongoDB


class Study:

    def __init__(self, user, flashcard_set, learned_terms=None, finished_session_time=None):
        self.user = user  # Передаем пользователя
        self.flashcard_set = flashcard_set  # Передаем набор карточек

        # создаём или получаем сессию изучения
        self.session, _ = StudySession.objects.get_or_create(
            user=user,
            flashcard_set=flashcard_set
        )

        # оптимизирован собственным менеджером, оптимизации не нуждается
        self.terms = flashcard_set.cards.all()  # получаем карточки связанные с набором карточек

        self.learned_terms = learned_terms or []
        self.finished_session_time = finished_session_time

    def is_known(self, term):
        """Проверяет, знает ли пользователь термин"""

        obj, _ = CardProgress.objects.get_or_create(
            user=self.user,
            card=term
        )
        return obj.is_known

    def get_terms_for_learning(self):
        """Возвращает список слов, которые пользователь ещё не знает"""

        return [term for term in self.terms if not self.is_known(term)]

    def save_learned_terms(self):
        """Сохраняет прогресс пользователя"""

        for term in self.learned_terms:
            cp, _ = CardProgress.objects.get_or_create(
                user=self.user,
                card=term
            )

            cp.is_known = term.is_known
            cp.save()

            # снимаем слепок БД и сохраняем в MongoDB
            mongo.snapshot_cardprogress(cp)

    def finish_session(self):
        """Завершает учебную сессию"""

        if self.finished_session_time:
            self.session.end_time = self.finished_session_time

        self.session.save()

        # снимаем слепок БД и сохраняем в MongoDB
        mongo.snapshot_studysession(self.session)
