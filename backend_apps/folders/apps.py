from django.apps import AppConfig


class FoldersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend_apps.folders'

    def ready(self):
        """Импортируем сигналы при загрузке приложения"""
        import backend_apps.folders.signals