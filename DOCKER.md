# Docker — запуск Recall

Полный стек в контейнерах: **PostgreSQL**, **MongoDB**, **Redis**, **Elasticsearch**, **Django (Gunicorn)**, **React (nginx)**.

Версии зафиксированы в образах и `requirements.txt` / `package.json` — на сервере не нужно ставить Python, Node, Postgres и т.д. вручную.

## Быстрый старт

```bash
# 1. Скопировать env
cp .env.example .env
# Отредактировать .env: SECRET_KEY, DB_PASSWORD, OAuth-ключи (если нужны)

# 2. Собрать и поднять
docker compose up -d --build

# 3. Запустить проект 
docker compose start

# 3. Открыть в браузере
# http://localhost  (или порт из HTTP_PORT)
```

Первый запуск:
- миграции Django
- collectstatic
- создание суперпользователя (если заданы `DJANGO_SUPERUSER_*` в `.env`)
- пересборка индекса Elasticsearch

Админка: `http://localhost/my-secret-admin-panel/`

## Полезные команды

```bash
# Логи
docker compose logs -f backend
docker compose logs -f frontend

# Миграции вручную
docker compose exec backend python manage.py migrate

# Shell Django
docker compose exec backend python manage.py shell

# Пересобрать только backend после изменений кода
docker compose up -d --build backend

# Остановить и удалить контейнеры (данные в volumes сохранятся)
docker compose down

# Полный сброс данных
docker compose down -v
```

## Структура сервисов

| Сервис          | Порт внутри | Описание                    |
|-----------------|-------------|-----------------------------|
| frontend (nginx)| 80          | SPA + reverse proxy к API   |
| backend         | 8000        | Django + Gunicorn           |
| db              | 5432        | PostgreSQL 16               |
| mongo           | 27017       | MongoDB 7                   |
| redis           | 6379        | Redis 7                     |
| elasticsearch   | 9200        | Elasticsearch 8.15          |

Снаружи наружу проброшен только **frontend:80** (или `HTTP_PORT`). API доступен через nginx: `/api/`, медиа — `/files/`, static — `/django-static/`.

## Фронтенд и API URL

В Docker фронт ходит на **относительный** путь:

```
REACT_APP_BASE_URL=/api/v1
```

Nginx проксирует `/api/` → `backend:8000`. Для локальной разработки без Docker можно в `.env` / `.env.local` фронта указать:

```
REACT_APP_BASE_URL=http://127.0.0.1:8000/api/v1
```

После смены `REACT_APP_*` нужна пересборка фронта:

```bash
docker compose up -d --build frontend
```

## OAuth (Google / GitHub)

1. Создать приложения в Google Cloud / GitHub OAuth Apps.
2. Redirect URI (пример):
   - Google: `http://your-domain/api/v1/social/google/`
   - Frontend callback: `http://your-domain/auth/callback`
3. Прописать в `.env`:
   - `AUTH_GOOGLE_OAUTH2_KEY`, `AUTH_GOOGLE_OAUTH2_SECRET`, `GOOGLE_REDIRECT_URI`
   - `AUTH_GITHUB_KEY`, `AUTH_GITHUB_SECRET`
   - `REACT_APP_GOOGLE_CLIENT_ID`, `REACT_APP_GITHUB_CLIENT_ID`, `REACT_APP_REDIRECT_URI`
4. Пересобрать frontend.

## Production-советы

- Поставь сильный `SECRET_KEY` и `DB_PASSWORD`.
- `DEBUG=False`.
- Повесь HTTPS (Caddy / Traefik / nginx на хосте) перед контейнером frontend.
- Регулярные бэкапы volumes: `postgres_data`, `media_data`, `mongo_data`.
- Elasticsearch ест ~512 MB RAM — на слабом VPS можно временно отключить сервис и поиск (или увеличить `ES_JAVA_OPTS`).

## Обновление на сервере

```bash
git pull
docker compose up -d --build
```

Новые миграции применятся автоматически через `entrypoint.sh`.
