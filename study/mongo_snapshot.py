from pymongo import MongoClient
from datetime import datetime, timezone
from django.conf import settings


class MongoSnapshotService:
    """ Класс для подключения к MongoDB и предоставлению ей методов для заполнения данных.
        Используется паттерн singleton для гарантии одного подключения
    """
    __instance = None
    __initialized = False

    def __new__(cls, *args, **kwargs):
        """Контролируем что объект у класса только один"""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        """
            Инициализация подключения к MongoDB.
            Защита от повторной инициализации благодаря флагу __initialized.
        """
        if self.__initialized:
            return
        self.client = MongoClient(settings.MONGO_URI)  # создаём соединение с БД
        self.db = self.client[settings.MONGO_DB_NAME]  # выбираем базу и подключаемся к ней

        # Индексы создаем
        self.db["card_progress"].create_index([("user_id", 1), ("card_id", 1), ("date_answer", 1)])
        self.db["study_sessions"].create_index([("user_id", 1), ("flashcard_set_id", 1), ("end_time", 1)])

        self.__initialized = True  # помечаем как инициализированный

    def _save_snapshot(self, collection_name, data):
        """Сохраняет слепок модели в MongoDB"""
        data["_created_at"] = datetime.now(timezone.utc)
        try:
            self.db[collection_name].insert_one(data)
        except Exception as e:
            print(f"[Mongo ERROR]: {e}")

    def save_snapshot_cardprogress(self, obj):
        """Делаем слепок модели CardProgress"""
        self._save_snapshot("card_progress", {
            "user_id": obj.user.public_id,
            "card_id": obj.card.public_id,
            "is_known": obj.is_known,
            "date_answer": obj.date_answer.isoformat(),
        })

    def save_snapshot_studysession(self, obj):
        """Делаем слепок модели StudySession"""
        self._save_snapshot("study_sessions", {
            "user_id": obj.user.public_id,
            "flashcard_set_id": obj.flashcard_set.public_id,
            "start_time": obj.start_time.isoformat(),
            "end_time": obj.end_time.isoformat(),
            "cards_studied": obj.cards_studied,
            "cards_known": obj.cards_known,
        })

    def delete_cardprogress(self, user_id, card_id):
        """Удаление истории модели в MongoDB"""
        self.db["card_progress"].delete_many({"user_id": user_id, "card_id": card_id})

    def delete_studysession(self, user_id, flashcard_set_id):
        """Удаление истории сессии обучения в MongoDB"""
        self.db["study_sessions"].delete_many({"user_id": user_id, "flashcard_set_id": flashcard_set_id})

    def get_cardprogress_history(self, user_id, card_id):
        """Метод получение данных истории карточки прогресса"""
        return list(
            self.db["card_progress"].find(
                {"user_id": user_id, "card_id": card_id}
            )
        )

    def get_studysession_history(self, user_id, flashcard_set_id):
        """Метод получения истории сессии обучения"""
        return list(
            self.db["study_sessions"].find(
                {"user_id": user_id, "flashcard_set_id": flashcard_set_id}
            )
        )

    def close(self):
        """ Данный метод создан для тестов, что бы после
            тестирования закрывать сессию, в Django не использовать
        """
        if self.client:
            self.client.close()
