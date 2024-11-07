from tortoise import Model, fields, Tortoise, run_async
from typing import List, Optional


# Определяем промежуточную модель для связи "многие ко многим"
# между пользователями и адресами
class UserAddress(Model):
    user = fields.ForeignKeyField(
        "models.User",
        related_name="user_addresses",
        on_delete=fields.CASCADE)
    address = fields.ForeignKeyField(
        "models.Address",
        related_name="user_addresses",
        on_delete=fields.CASCADE)

    class Meta:
        table = "user_address"
        unique_together = (
        ("user", "address"),)  # уникальная пара user_id и address_id


# Основная модель User для реализации связей
class User(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=30, unique=True)
    fullname = fields.CharField(max_length=128, null=True)
    password = fields.CharField(max_length=30)
    email_address = fields.CharField(max_length=30)

    # Связь "многие ко многим" с Address через промежуточную таблицу user_address
    addresses: List["Address"] = fields.ManyToManyField(
        "models.Address", related_name="users",
        through=UserAddress
    )

    # Связь "один ко многим" с Invoice
    invoices: List["Invoice"] = fields.ReverseRelation["Invoice"]


# Модель Address для связи "многие ко многим" с User
class Address(Model):
    id = fields.IntField(primary_key=True)
    country = fields.CharField(max_length=50)
    city = fields.CharField(max_length=50)
    street = fields.CharField(max_length=100)
    house_number = fields.CharField(max_length=20)


# Модель Invoice для связи "один ко многим" с User
class Invoice(Model):
    id = fields.IntField(primary_key=True)
    price = fields.DecimalField(max_digits=10, decimal_places=2)

    # ForeignKey для связи с User
    user: User = fields.ForeignKeyField(
        "models.User",
        related_name="invoices",
        on_delete=fields.CASCADE
    )


# Модель Profile для связи "один к одному" с User
class Profile(Model):
    id = fields.IntField(primary_key=True)
    bio = fields.TextField()
    avatar_url = fields.CharField(max_length=200, null=True)

    # ForeignKey для связи с User
    user: User = fields.OneToOneField(
        "models.User",
        related_name="profile",
        on_delete=fields.CASCADE
    )

#
# async def init():
#     await Tortoise.init(
#         db_url='sqlite://test.db',
#         modules={'models': ['__main__']}  # Импортируйте ваши модели здесь
#     )
#     await Tortoise.generate_schemas()
#
#     # Пример создания пользователя и его профиля
#     user = await User.create(
#         username="john_doe",
#         password="secure_password",
#         email_address="john@example.com")
#     profile = await Profile.create(
#         user=user,
#         bio="Hello, I'm John!",
#         avatar_url="http://example.com/avatar.jpg")
#
#     print(f"Created user: {user.username}, Profile bio: {profile.bio}")
#
#     await Tortoise.close_connections()
#
#
# if __name__ == "__main__":
#     run_async(init())
