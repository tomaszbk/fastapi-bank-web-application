import random
from datetime import datetime

from app.infrastructure.models import User, BankAccount
from app.services.auth_service import auth
from app.services.transaction_service import create_transaction


def generate_numbers():
    num = 1
    while True:
        yield num
        num += 1


number_gen = generate_numbers()


def user_factory() -> User:
    username = f"user{next(number_gen)}"

    return User(
        username=username,
        name=f"{username}_name",
        surname=f"{username}_surname",
        dni=random.randint(100000, 999999),
        age=random.randint(18, 99),
        email=f"{username}@example.com",
        hashed_password=auth.hash_password("test123"),
        creation_date=datetime.now(),
        last_updated=datetime.now(),
    )


def bank_account_factory() -> BankAccount:
    return BankAccount(balance=random.randint(1000, 10000), creation_date=datetime.now())


def random_transactions_generator(session, iterations: int, users: list[User]) -> None:
    for _ in range(iterations):
        try:
            user1 = random.choice(users)
            user2 = random.choice(users)
            amount = random.randint(100, 10000)
            create_transaction(session, user1, amount, user2)
        except Exception as ex:
            session.rollback()
            print(f"error: {ex}")
