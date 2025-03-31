# MySite - Кастомная CRM на Django

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.0+-green.svg)](https://www.djangoproject.com/)

Разрабатываю кастомную CRM-систему на Django для управления контентом и пользователями.

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ваш-username/my_site.git
cd my_site
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
# Linux/MacOS:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте базу данных в `settings.py`

5. Выполните миграции:
```bash
python manage.py migrate
```

6. Создайте администратора:
```bash
python manage.py createsuperuser
```

7. Запустите сервер:
```bash
python manage.py runserver
```

Откройте в браузере: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Основные команды

| Команда | Описание |
|---------|----------|
| `python manage.py runserver` | Запуск сервера разработки |
| `python manage.py makemigrations` | Создание миграций |
| `python manage.py migrate` | Применение миграций |
| `python manage.py collectstatic` | Сбор статических файлов |