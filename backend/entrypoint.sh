#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
until python -c "
import os, sys
import psycopg2
try:
    psycopg2.connect(
        dbname=os.environ.get('DB_NAME', 'recall'),
        user=os.environ.get('DB_USER', 'recall'),
        password=os.environ.get('DB_PASSWORD', 'recall'),
        host=os.environ.get('DB_HOST', 'db'),
        port=os.environ.get('DB_PORT', '5432'),
        connect_timeout=3,
    )
except Exception as e:
    sys.exit(1)
sys.exit(0)
" 2>/dev/null; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done
echo "PostgreSQL is up"

echo "Waiting for Redis..."
until python -c "
import os, redis, sys
r = redis.from_url(os.environ.get('REDIS_URL', 'redis://redis:6379/1'))
r.ping()
" 2>/dev/null; do
  echo "Redis is unavailable - sleeping"
  sleep 2
done
echo "Redis is up"

echo "Waiting for Elasticsearch..."
until curl -sf "${ELASTIC_HOST:-http://elasticsearch:9200}/_cluster/health" >/dev/null 2>&1; do
  echo "Elasticsearch is unavailable - sleeping"
  sleep 3
done
echo "Elasticsearch is up"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Optional: create superuser if env vars set and none exists
if [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='$DJANGO_SUPERUSER_EMAIL').exists():
    User.objects.create_superuser(
        username='${DJANGO_SUPERUSER_USERNAME:-admin}',
        email='$DJANGO_SUPERUSER_EMAIL',
        password='$DJANGO_SUPERUSER_PASSWORD',
        first_name='Admin',
        last_name='User',
        is_active=True,
        is_email_verified=True,
    )
    print('Superuser created')
else:
    print('Superuser already exists')
" || true
fi

# Rebuild ES index (safe if empty)
python manage.py search_index --rebuild -f 2>/dev/null || echo "ES index rebuild skipped (no documents or command unavailable)"

exec "$@"
