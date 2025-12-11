import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from backend_apps.media.models import Image, Sound


# TODO: Замени функцию print() на логирование,
#  что бы видеть если в логах если файл не был удален
@receiver(pre_delete, sender=Image)
@receiver(pre_delete, sender=Sound)
def delete_files(sender, instance, **kwargs):
    """Удаление файлов, если сама модель удалена"""

    file_path = instance.path_file.path  # абсолютный путь к файлу

    if not os.path.isfile(file_path):
        print(f"Файл {file_path} не найден — возможно, уже был удалён.")
        return
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Ошибка при удалении файла {file_path}: {e}")
