# Table of Contents
1. [Функционал приложения](#функционал-приложения)
2. [Используемый стек технологий](#используемый-стек-технологий)
3. [Инструкция для запуска](#инструкция-для-запуска) 
   1. [Переменные окружения](#переменные-окружения)
   2. [Инструкции БД и суперпользователя](#выполните-инструкции-для-создания-и-наполнения-базы-данных-и-создания-суперпользователя)
   3. [Запуск Djsngo-server](#запустите-сервер-django)
4. [Инструкция Docker](#docker---инструкция-по-запуску)
   1. [Запуск docker](#запуск-docker)

    
# Функционал приложения.

Личный блог с возможностью комментирования постов. Есть возможность подписки на
RSS ленту. Реализован функционал отправки постов по почте. Преобразует посты,
написанные на markdown в html на сайте. Присутствуют теги и различная 
фильтрация/комбинация по ним. Есть полнотекстовый поиск по постам.

# Используемый стек технологий.
- Python
- Django
- markdown

# Инструкция для запуска.

## Переменные окружения.
**В корневой папке создать файл расширения _.env_**
```
SECRET_KEY=XXXXXX
DEBUG=XXXX
ALLOWED_HOSTS=XXXXXX XXXXXXX # Перечислить все необходимые хосты через пробел.
```
Для базы данных Postgresql указать следуюшие переменные:
```
POSTGRES_DB=XXXXXXXX
POSTGRES_USER=XXXXXXXX
POSTGRES_PASSWORD=XXXXXXXX
DB_HOST=XXXXXXXX
DB_PORT=XXXX
```
Для работы почты укажите в переменных настройки приложения для вашей почты
```
EMAIL_HOST=XXXXXXXX
EMAIL_HOST_USER=XXXXXXXX
EMAIL_HOST_PASSWORD=XXXXXXXX
EMAIL_PORT=XXXXXXXX
DEFAULT_FROM_EMAIL=XXXXXXXX
```

## Выполните инструкции для создания и наполнения базы данных и создания суперпользователя:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Запустите сервер Django:

```
python manage.py runserver
```

**По умолчанию проект работает на порту 8000.**

# Docker - инструкция по запуску

*База данных Postgres работает в контейнере docker*

### Запуск Docker
Запустить из корневой папки в терминале:
```
docker run --name=XXXX -e POSRGRES_DB=XXXX -e POSTGRES_USER=XXXX -e
POSTGRES_PASSWORD=XXXX -p XXXX:5432 -d postgres
```
Сайт будет доступен на порту:
http://localhost:8000