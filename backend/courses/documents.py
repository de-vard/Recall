from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Course


# Декоратор @registry.register_document автоматически регистрирует этот класс
# как документ, связанный с индексом Elasticsearch
@registry.register_document
class CourseDocument(Document):
    """ CourseDocument — это класс, который описывает, как данные из модели Course
        будут представляться и индексироваться в Elasticsearch.
    """

    # Явно определяем поля, которые хотим индексировать с особым поведением
    title = fields.TextField(attr='title', analyzer='russian')
    description = fields.TextField(attr='description', analyzer='russian')

    # Вложенный класс Index — описывает настройки самого индекса в Elasticsearch
    class Index:
        name = 'courses'
        settings = {
            'number_of_shards': 1,  # Количество частей индекса, 1 — нормально для небольших и средних объёмов данных
            'number_of_replicas': 1,  # количество копий каждого шарда, 1 — стандарт для продакшена (отказоустойчивость)
        }

    # Вложенный класс Django — связывает документ с моделью Django
    class Django:
        model = Course

        # Список полей модели, которые будут автоматически индексироваться
        # Эти поля попадут в Elasticsearch как есть (без специальной обработки)
        # Если поле уже определено выше (title, description), то оно НЕ будет дублироваться
        fields = [
            'public_id',
            'is_public',
            'created',
        ]

        # ignore_signals = False → означает, что сигналы Django (post_save, post_delete и т.д.)
        # будут перехватываться и автоматически обновлять индекс в Elasticsearch
        # Если поставить True — синхронизация работать НЕ будет
        ignore_signals = False

        # auto_refresh = True → после сохранения изменения сразу видны в поиске
        # (Elasticsearch делает refresh индекса)
        # В продакшене часто ставят False для лучшей производительности
        auto_refresh = True  # удобно для разработки

        # При массовой индексации (например, при --populate) объекты будут браться
        # порциями по 5000 штук — это помогает не перегружать память
        queryset_pagination = 5000
