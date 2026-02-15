# Recall

**Recall** — это умное веб-приложение для эффективного запоминания информации с использованием научно доказанной методики **интервальных повторений (Spaced Repetition System, SRS)**. Приложение помогает систематизировать и надолго закреплять знания, будь то изучение языка, подготовка к экзаменам или запоминание фактов.

[![Django](https://img.shields.io/badge/Django-5.2.6-green?logo=django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.16.1-red)](https://www.django-rest-framework.org/)
[![React](https://img.shields.io/badge/React-18.x-blue?logo=react)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16.x-blue?logo=postgresql)](https://www.postgresql.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.x-green?logo=mongodb)](https://www.mongodb.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Возможности

*   🧠 **Интервальные повторения (SRS)**: Умный алгоритм для эффективного запоминания
*   📚 **Иерархическая структура**: Курсы → Папки → Модули → Карточки
*   🔍 **Полнотекстовый поиск по курсам**: Быстрый и релевантный поиск по названию и описанию курсов на базе **Elasticsearch** (с поддержкой русского языка, опечаток и приоритетом заголовка)  
*   🎵 **Поддержка аудио**: Специальное поле для хранения и воспроизведения звуковых файлов
*   📊 **История изучения**: Отслеживание прогресса и статистика повторений
*   🔐 **JWT-аутентификация**: Безопасная авторизация с автоматическим обновлением токенов
*   📖 **Документация API**: Полная документация через Swagger/DRF-YASG
*   ⚡ **Производительность**: Оптимизация запросов, профайлинг с Django Silk
*   🔗 **Регистрация и вход через социальные сети**: Google и GitHub OAuth2 с автоматическим созданием пользователя и загрузкой аватара
*   🎨 **Современный интерфейс**: Адаптивный дизайн на React

## 🛠️ Технологический стек

### **Backend (Django REST Framework)**
- **Фреймворк**: Django 5.2.6 + Django REST Framework 3.16.1
- **Базы данных**:
  - PostgreSQL 
  - MongoDB 
- **Аутентификация**: JWT (djangorestframework-simplejwt)
- **Документация API**: DRF-YASG (Swagger)
- **Оптимизация и мониторинг**:
  - Django Silk — профайлинг запросов
  - Django Debug Toolbar
  - Оптимизированные запросы с `select_related`, `prefetch_related`
- **Поисковый движок**: **Elasticsearch** + django-elasticsearch-dsl
  - Полнотекстовый поиск по курсам (название + описание)
  - Русский анализатор, поддержка опечаток (fuzziness), приоритет заголовка (boost)
  - Автоматическая синхронизация при создании/изменении курсов
- **Валидация**: Кастомные валидаторы (SizeValueValidator)
- **Медиафайлы**: Кастомное поле модели SoundField для работы с аудио
- **Сигналы**: Django signals для автоматических действий
- **Тестирование**: pytest 

### **Frontend (React + TypeScript)**
- **Фреймворк**: React 18 + TypeScript
- **Маршрутизация**: React Router DOM
- **HTTP-клиент**: Axios с автоматическим обновлением JWT-токенов
- **Интерцепторы**: 
  - Автоматическая подстановка токена в заголовки
  - Refresh token логика при 401 ошибках
  - Редирект на логин при истечении сессии
- **Архитектура**: Кастомные хуки для работы с API (useCard, useFolder и т.д.)
- **Стилизация**: CSS Modules / Tailwind CSS
- **Состояние**: Локальный state через useState, глобальное через Context API

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

---
⭐ **Если проект вам понравился, не забудьте поставить звезду на GitHub!** Это мотивирует на дальнейшую разработку.