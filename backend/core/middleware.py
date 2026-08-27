from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection


class OnlineStatusMiddleware(MiddlewareMixin):
    """ Middleware, который обновляет время последней активности пользователя в Redis.
        Используется для отображения "кто сейчас онлайн" на сайте.
    """
    def process_response(self, request, response):
        """ Этот метод вызывается после формирования ответа, но перед отправкой клиенту.
            Здесь мы отмечаем, что пользователь был активен именно в этот момент.
        """
        # Пропускаем неавторизованных пользователей — они не считаются "онлайн"
        if not request.user.is_authenticated:
            return response

        # Фильтруем ненужных пользователей
        if request.user.is_staff:
            return response

        try:
            # Получаем соединение с Redis (должно быть настроено в CACHES с именем "default")
            r = get_redis_connection("default")

            # Преобразуем ID пользователя в строку — Redis работает со строковыми ключами
            user_id = str(request.user.public_id)

            # Текущее время в формате Unix timestamp (секунды с 1970 года)
            now = int(timezone.now().timestamp())

            # Используем pipeline — это быстрее, когда нужно выполнить несколько команд
            pipe = r.pipeline()

            # Добавляем/обновляем запись в отсортированном множестве (Sorted Set)
            # Ключ = ID пользователя
            # Score = timestamp последнего захода
            # Если пользователь уже был → просто обновится время
            pipe.zadd("online_users", {user_id: now})

            # Выполняем все команды из pipeline одним запросом к Redis
            pipe.execute()

        except Exception:
            # Если Redis недоступен (упал, таймаут, ошибка сети и т.д.)
            # → молча игнорируем, чтобы не ломать весь сайт из-за этого
            pass  # Redis упал — не ломаем сайт

        return response
