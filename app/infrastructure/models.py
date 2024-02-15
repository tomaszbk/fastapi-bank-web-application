from sqlalchemy import CheckConstraint, Integer, String, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy import DateTime, Double, ForeignKeyConstraint
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column as column,
    Mapped as M,
    MappedAsDataclass,
    relationship,
)
from datetime import datetime
from typing import List

from app.infrastructure.engine import postgres_session_factory


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""


# back populates is how the table is represented in the relationed table


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="users_pkey"),
        UniqueConstraint("username", name="users_username_key"),
    )

    id: M[int] = column(Integer, init=False)
    username: M[str] = column(String(50), nullable=False)
    name: M[str] = column(String(50), nullable=False)
    surname: M[str] = column(String(50), nullable=False)
    hashed_password: M[str] = column(String(255), nullable=False)
    email: M[str] = column(String(50), nullable=False)
    cuit: M[int] = column(String(50), nullable=False)
    age: M[int] = column(Integer, nullable=False)
    creation_date: M[datetime] = column(DateTime, nullable=False)
    last_updated: M[datetime] = column(DateTime, nullable=False)

    bank_account: M["BankAccount"] = relationship(
        "BankAccount", uselist=False, back_populates="user", init=False
    )


class BankAccount(Base):
    __tablename__ = "bank_accounts"
    __table_args__ = (
        CheckConstraint("balance >= 0", name="bank_accounts_balance_check"),
        ForeignKeyConstraint(["user_id"], ["users.id"], name="bank_accounts_user_id_fkey"),
        PrimaryKeyConstraint("id", name="bank_accounts_pkey"),
        UniqueConstraint("user_id", name="bank_accounts_user_id_key"),
    )

    id: M[int] = column(Integer, init=False)
    cbu: M[str] = column(String(22), nullable=False, init=False)
    user_id: M[int] = column(Integer, nullable=False, init=False)
    balance: M[float] = column(Double(53))
    creation_date: M[datetime] = column(DateTime, nullable=False)
    bank_id: M[int] = column(Integer, nullable=False, init=False)
    bank: M["Bank"] = relationship("Bank", back_populates="accounts", init=False)
    user: M["User"] = relationship("User", back_populates="bank_account", init=False)
    origin_transactions: M[List["Transaction"]] = relationship(
        "Transaction",
        uselist=True,
        foreign_keys="[Transaction.origin_account_id]",
        back_populates="origin_account",
        init=False,
    )
    destiny_transactions: M[List["Transaction"]] = relationship(
        "Transaction",
        uselist=True,
        foreign_keys="[Transaction.destination_account_id]",
        back_populates="destination_account",
        init=False,
    )


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["destination_account_id"],
            ["bank_accounts.id"],
            name="transactions_destination_account_id_fkey",
        ),
        ForeignKeyConstraint(
            ["origin_account_id"], ["bank_accounts.id"], name="transactions_origin_account_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="transactions_pkey"),
    )

    id: M[int] = column(Integer, init=False)
    number: M[str] = column(String(50), nullable=False)
    origin_account_id: M[int] = column(Integer, nullable=False, init=False)
    destination_account_id: M[int] = column(Integer, nullable=False, init=False)
    amount: M[float] = column(Double(53), nullable=False)
    date: M[datetime] = column(DateTime, nullable=False)

    origin_account: M["BankAccount"] = relationship(
        "BankAccount",
        foreign_keys=[origin_account_id],
        back_populates="origin_transactions",
        init=False,
    )
    destination_account: M["BankAccount"] = relationship(
        "BankAccount",
        foreign_keys=[destination_account_id],
        back_populates="destiny_transactions",
        init=False,
    )


class Bank(Base):
    __tablename__ = "banks"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="banks_pkey"),
        UniqueConstraint("name", name="banks_name_key"),
    )

    id: M[int] = column(Integer, init=False)
    code: M[str] = column(String(10), nullable=False)
    name: M[str] = column(String(50), nullable=False)

    accounts: M[List["BankAccount"]] = relationship(
        "BankAccount", back_populates="bank", init=False
    )


engine = postgres_session_factory.engine
Base.metadata.create_all(engine)

external_banks = {"0000000001": "Milagro Financiero", "0000000003": "Generacion"}
bank_of_tomorrow = Bank(code="0000000002", name="Bank of Tomorrow")

with postgres_session_factory.Session() as session:
    for bank in external_banks:
        session.add(Bank(code=bank, name=external_banks[bank]))
    session.add(bank_of_tomorrow)
    session.commit()
