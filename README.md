# Проект с использованием Tortoise ORM

Этот проект использует Tortoise ORM для работы с базой данных.
Tortoise ORM — это асинхронная ORM для Python, которая предоставляет 
удобные средства для работы с базами данных в асинхронных приложениях.

## Требования

Для начала работы с проектом необходимо установить несколько зависимостей:

### Требования

- Python 3.8+
- pip
- Virtualenv (рекомендуется для изоляции окружения)

### Шаги по установке

1. **Клонировать репозиторий:**

   ```bash
   git clone https://github.com/KVoff/Django_diplom.git

2. **Создайте и активируйте виртуальное окружение:**
   На Windows:
    ```bash
   python -m venv venv
   venv\Scripts\activate

На Mac/Linux:

    python3 -m venv venv
    source venv/bin/activate

3. **Установите зависимости проекта:**

    ```bash
   pip install -r requirements.txt

4. **Настройте базу данных:**
   Используется SQLite (по умолчанию)

5. **После этого выполните миграции:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate

6. **Запустите сервер разработки:**
После этого сервер будет доступен по адресу: http://127.0.0.1:8000/.


7. **Запуск тестов:**
   ```bash
    python manage.py test -v2    

-v2 нужен для отображения принтов в тестах