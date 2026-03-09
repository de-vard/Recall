from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection


class OnlineStatusMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if not request.user.is_authenticated:
            return response

        # Фильтруем ненужных пользователей
        if request.user.is_staff:
            return response
        # Если есть поле is_bot — используй его
        # if hasattr(request.user, 'is_bot') and request.user.is_bot:
        #     return response

        try:
            r = get_redis_connection("default")
            user_id = str(request.user.id)
            now = int(timezone.now().timestamp())

            pipe = r.pipeline()
            pipe.zadd("online_users", {user_id: now})
            # pipe.expire("online_users", 86400 * 7)   # опционально — 7 дней страховка
            pipe.execute()

        except Exception:
            pass  # Redis упал — не ломаем сайт

        return response
