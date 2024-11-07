import asyncio
import logging
import os
import time

import pytest
from tortoise import Tortoise
from models import User, Profile, Address, Invoice

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Настройка обработчика для записи логов в файл
file_handler = logging.FileHandler('test_logs.log', mode='w')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(console_handler)

db_path = "test.db"


@pytest.fixture(scope='function', autouse=True)
async def init_db():
    try:
        # Инициализация базы данных перед тестами
        await Tortoise.init(
            db_url="sqlite://test.db",
            modules={"models": ["models"]}
        )
        await Tortoise.generate_schemas()  # Генерация схем базы данных
    except Exception as e:
        logger.error(f"Ошибка инициализации базы данных: {e}")
        raise
    yield  # Позволяет выполнять тесты

    await Tortoise.close_connections()  # Закрытие соединений после тестов


@pytest.fixture(scope='function')
async def fill_db():
    # Заполнение базы данных начальными данными
    users = []
    for i in range(10):
        user = await User.create(
            username=f'Test_user_{i}',
            password=f'123456_{i}',
            email_address=f'test{i}@localhost',
            fullname=f'Test User {i}',
        )
        users.append(user)

    for i in range(10):
        await Address.create(
            country='Russia',
            city=f'City_{i}',
            street=f'Street_{i}',
            house_number=f'{i}'
        )

    for i in range(10):
        await Invoice.create(
            price=100 + i * 10,
            user=users[i]  # Связываем инвойс с пользователем
        )

    for i in range(10):
        await Profile.create(
            bio=f'Bio of User {i}',
            avatar_url=f'https://example.com/avatar_{i}.png',
            user=users[i]  # Связываем профиль с пользователем
        )

    yield  # Возвращаем контроль тестам


@pytest.mark.asyncio
class TestCreate:

    async def test_fill_db(self, fill_db):
        try:

            user_count = await User.all().count()
            assert user_count == 10, logger.error(
                f'Ошибка: ожидалось 10 профилей,'
                f'но было найдено {user_count}'
            )

            logger.info('Создано 10 пользователей в базе данных')

            address_count = await Address.all().count()
            assert address_count == 10, logger.error(
                f'Ошибка: ожидалось 10 адресов,'
                f'но было найдено {address_count}'
            )
            logger.info('Создано 10 адресов в базе данных')

            invoice_count = await Invoice.all().count()
            assert invoice_count == 10, logger.error(
                f'Ошибка: ожидалось 10 инвойсов,'
                f'но было найдено {invoice_count}'
            )
            logger.info('Создано 10 инвойсов в базе данных')

            profile_count = await Profile.all().count()

            assert profile_count == 10, (
                f'Ошибка: ожидалось 10 профилей,'
                f'но было найдено {profile_count}'
            )





        finally:
            # Удаление всех записей после проверки
            await User.all().delete()
            await Address.all().delete()
            await Invoice.all().delete()
            await Profile.all().delete()

            # Проверка что база данных пуста
            user_count = await User.all().count()
            assert user_count == 0
            logger.info('Все пользователи удалены из базы данных')


@pytest.mark.asyncio
class TestCrud:
    logger.info(
        f" \n ===== Current time: {time.ctime()} ===== \n")

    # CREATE
    async def test_create_users(self):
        start_time = time.time()

        users_count = 0
        for i in range(100_000):
            await User.create(
                username=f"NewUser_{i}",
                password="password123",
                email_address=f"newuser{i}@example.com",
                fullname=f"New User {i}"
            )
            users_count += 1

        logger.info(
            f"Create {users_count} users in SQLA: {time.time() - start_time} "
            f"seconds")

    # READ
    async def test_read_all_users(self):
        start_time = time.time()
        users = await User.all()

        logger.info(
            f"READ {len(users)} users in SQLA: {time.time() - start_time} "
            f"seconds")

    # UPDATE (Обновление)
    async def test_update_users(self):
        start_time = time.time()

        # Загружаем всех пользователей за один запрос
        users = await User.all().update(fullname="Updated User")

        # # Изменяем пользователей
        # for user in users:
        #     user.fullname = f"Updated User {user}"
        #
        #     await user.save()

        logger.info(
            f"UPDATE {users} in SQLA: {time.time() - start_time} "
            f"seconds")

    # DELETE ALL USERS
    async def test_delete_all_users(self):
        start_time = time.time()

        await User.all().delete()

        logger.info(
            f'Удалены все пользователи. Время выполнения: '
            f'{time.time() - start_time} seconds')

        user_count = await User.all().count()
        assert user_count == 0
