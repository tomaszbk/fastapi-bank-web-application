from datetime import datetime
from typing import Optional

from sqlmodel import (
    CheckConstraint,
    Field,
    Relationship,
    SQLModel,
)


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    name: str
    surname: str
    hashed_password: str
    email: str
    dni: str
    age: int
    creation_date: datetime
    last_updated: datetime
    last_login: Optional[datetime] = None

    bank_account: Optional["Account"] = Relationship(back_populates="user")


class Account(SQLModel, table=True):
    __tablename__ = "accounts"
    __table_args__ = (CheckConstraint("balance >= 0", name="accounts_balance_check"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, unique=True, foreign_key="users.id")

    balance: float
    creation_date: datetime

    user: Optional[User] = Relationship(back_populates="bank_account")
    origin_transactions: list["Transaction"] = Relationship(
        back_populates="origin_account",
        sa_relationship_kwargs={"foreign_keys": "Transaction.origin_account_id"},
    )
    destination_transactions: list["Transaction"] = Relationship(
        back_populates="destination_account",
        sa_relationship_kwargs={"foreign_keys": "Transaction.destination_account_id"},
    )


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    origin_account_id: int = Field(default=None, foreign_key="accounts.id")
    destination_account_id: int = Field(default=None, foreign_key="accounts.id")

    amount: float
    transaction_date: datetime

    origin_account: Optional[Account] = Relationship(
        back_populates="origin_transactions",
        sa_relationship_kwargs={"foreign_keys": "Transaction.origin_account_id"},
    )
    destination_account: Optional[Account] = Relationship(
        back_populates="destination_transactions",
        sa_relationship_kwargs={"foreign_keys": "Transaction.destination_account_id"},
    )


metadata = SQLModel.metadata
