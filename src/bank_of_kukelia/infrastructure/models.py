from sqlalchemy import  Integer, String, MetaData, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy import DateTime, Double, ForeignKeyConstraint
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, MappedAsDataclass, relationship

from datetime import datetime
from typing import List

metadata = MetaData()


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""

#back populates is how the table is represented in the relationed table

class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('username', name='users_username_key')
    )

    id: Mapped[int] = mapped_column(Integer, init=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    dni: Mapped[int] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    creation_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    last_updated: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    last_login: Mapped[datetime] = mapped_column(DateTime, init=False)

    bank_account: Mapped['BankAccount'] = relationship('BankAccount', uselist=False, back_populates='user', init=False)


class BankAccount(Base):
    __tablename__ = 'bank_accounts'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], name='bank_accounts_user_id_fkey'),
        PrimaryKeyConstraint('id', name='bank_accounts_pkey'),
        UniqueConstraint('user_id', name='bank_accounts_user_id_key')
    )

    id: Mapped[int] = mapped_column(Integer, init=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, init=False)
    balance: Mapped[float] = mapped_column(Double(53), nullable=False)
    creation_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='bank_account', init=False)
    origin_transactions: Mapped[List['Transaction']] = relationship('Transaction', uselist=True, foreign_keys='[Transaction.destination_account_id]', back_populates='destination_account', init=False)
    destiny_transactions_: Mapped[List['Transaction']] = relationship('Transaction', uselist=True, foreign_keys='[Transaction.origin_account_id]', back_populates='origin_account', init=False)


class Transaction(Base):
    __tablename__ = 'transactions'
    __table_args__ = (
        ForeignKeyConstraint(['destination_account_id'], ['bank_accounts.id'], name='transactions_destination_account_id_fkey'),
        ForeignKeyConstraint(['origin_account_id'], ['bank_accounts.id'], name='transactions_origin_account_id_fkey'),
        PrimaryKeyConstraint('id', name='transactions_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, init=False)
    origin_account_id: Mapped[int] = mapped_column(Integer, nullable=False, init=False)
    destination_account_id: Mapped[int] = mapped_column(Integer, nullable=False, init=False)
    amount: Mapped[float] = mapped_column(Double(53), nullable=False)
    transaction_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    origin_account: Mapped['BankAccount'] = relationship('BankAccount', foreign_keys=[origin_account_id], back_populates='origin_transactions', init=False)
    destination_account: Mapped['BankAccount'] = relationship('BankAccount', foreign_keys=[destination_account_id], back_populates='destiny_transactions_', init=False)
