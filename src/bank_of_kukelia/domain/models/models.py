from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    name: str
    surname: str
    username: str
    hashed_password: str
    dni: int
    age: int
    email: str


@dataclass
class BankAccount:
    user: User
    creation_date: datetime
    balance: float = 100000


@dataclass
class Operation:
    origin_account: BankAccount
    destination_account: BankAccount
    amount: float
