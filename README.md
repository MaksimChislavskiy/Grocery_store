# Grocery_store
# Магазин продуктов API

API для интернет-магазина продуктов с корзиной, категориями и товарами.

## Функционал

- Управление категориями и подкатегориями (админка)
- Управление товарами с изображениями в трех размерах (админка)
- Просмотр категорий с вложенными подкатегориями (пагинация)
- Просмотр товаров с пагинацией
- Корзина для авторизованных пользователей:
  - Добавление товара
  - Изменение количества
  - Удаление товара
  - Полная очистка
  - Просмотр состава с подсчетом суммы и количества
- Аутентификация по токену
- Swagger документация

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone <repo-url>
   cd shop_project
2. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
4. Примените миграции:
    ```bash
    python manage.py migrate
5. Создайте суперпользователя:
    ```bash
    python manage.py createsuperuser
6. Загрузите фикстуры (опционально):
    ```bash
    python manage.py load_fixtures
7. Запустите сервер разработки:
    ```bash
    python manage.py runserver

## Swagger
После запуска сервера документация доступна по адресу:

- Swagger UI: http://localhost:8000/swagger/

- ReDoc: http://localhost:8000/redoc/

## Тестирование
Запуск тестов:
    ```bash
    python manage.py test