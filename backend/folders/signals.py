from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from folders.models import Folder

User = get_user_model()


@receiver(post_save, sender=User)
def post_save_dispatcher(sender, instance, created, **kwargs):
    """Сигнал, который создает пользователю корневую папку"""
    if created:
        Folder.objects.create(
            title='home',  # Название пользователя
            owner=instance,  # Указываем пользователя
            parent_folder=None  # Явно указываем, что это корневая папка
        )
