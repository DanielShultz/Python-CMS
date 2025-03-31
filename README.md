# MySite - Кастомная CRM на Django

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.0+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Разрабатываю кастомную CRM-систему на Django с расширенными возможностями для управления контентом, пользователями и взаимодействиями.

## 🌟 Особенности

- Многофункциональная система управления контентом
- Гибкая система типов и категорий
- 10-балльная система рейтингов и лайков
- Комментарии и взаимодействия пользователей
- Адаптивный дизайн с поддержкой мобильных устройств
- Карусель баннеров и промо-материалов

## 🚀 Быстрый старт

### Предварительные требования
- Python 3.8+
- PostgreSQL (рекомендуется) или SQLite
- Виртуальное окружение (рекомендуется)

### Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш-username/my_site.git
   cd my_site
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Настройте базу данных в `settings.py` (по умолчанию используется SQLite)

5. Примените миграции:
   ```bash
   python manage.py migrate
   ```

6. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```

7. Запустите сервер разработки:
   ```bash
   python manage.py runserver
   ```

8. Откройте в браузере: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 🛠 Команды разработки

- Запуск тестов: `python manage.py test`
- Создание миграций: `python manage.py makemigrations`
- Запуск с отладочной панелью: `python manage.py runserver --insecure`
- Сбор статики: `python manage.py collectstatic`