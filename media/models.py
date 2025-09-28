import uuid

from django.db import models



class Image(models.Model):
    """Модель для хранения изобразения"""
    public = models.UUIDField(
        db_index=True,  # Ускоряет поиск по public_id.
        unique=True,  # Запрещает дубликаты.
        default=uuid.uuid4,  # Автоматически генерирует UUID.
        editable=False,  # Нельзя изменить вручную.
    )
    title = models.CharField(verbose_name="Название", max_length=255)
    image_file = models.ImageField(verbose_name="Сылка на файл", upload_to="images/%Y/%m/%d")
    uploaded_by_user = models.ForeignKey(
        'users.User',
        verbose_name="Кто загрузил изображение",
        on_delete=models.CASCADE,
        related_name="+", # отключаем атрибут для экономии системных ресурсов
    )
    created = models.DateTimeField(verbose_name="Дата регистрации",auto_now_add=True)
