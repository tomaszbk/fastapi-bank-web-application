from src.bank_of_kukelia.infrastructure.models import User
from bank_of_kukelia.services.auth_service import auth
import random
from datetime import datetime


def generate_numbers():
    num = 1
    while True:
        yield num
        num += 1

number_gen = generate_numbers()


def user_factory() -> User:
    username = f"user{next(number_gen)}"

    return User(username = username,
        name = f"{username}_name",
        surname = f"{username}_surname",
        dni = random.randint(100000, 999999),
        age = random.randint(18, 99),
        email = f"{username}@example.com",
        hashed_password = auth.hash_password("test123"),
        creation_date = datetime.now(),
        last_updated = datetime.now()
        )
