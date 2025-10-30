from pymongo import MongoClient
from datetime import datetime, timezone
from django.conf import settings


class MongoSnapshotService:
    """Класс для подключения к MongoDB и предоставлению ей методов для заполнения данных"""
    # Подключение к MongoDB
    client = MongoClient(settings.MONGO_URI)  # создаём соединение
    db = client[settings.MONGO_DB_NAME]  # выбираем базу

    # todo: реализуй индексы
    def save_snapshot(self, collection_name, data):
        """Сохраняет слепок модели в MongoDB"""
        data["_created_at"] = datetime.now(timezone.utc)
        try:
            self.db[collection_name].insert_one(data)
        except Exception as e:
            print(f"[Mongo ERROR]: {e}")

    def snapshot_cardprogress(self, obj):
        """Делаем слепок модели CardProgress"""
        self.save_snapshot("card_progress", {
            "user_id": obj.user.public_id,
            "card_id": obj.card.public_id,
            "is_known": obj.is_known,
            "date_answer": obj.date_answer.isoformat(),
        })

    def snapshot_studysession(self, obj):
        """Делаем слепок модели StudySession"""
        self.save_snapshot("study_sessions", {
            "user_id": obj.user.public_id,
            "flashcard_set_id": obj.flashcard_set.public_id,
            "start_time": obj.start_time.isoformat(),
            "end_time": obj.end_time.isoformat(),
            "cards_studied": obj.cards_studied,
            "cards_known": obj.cards_known,
        })

