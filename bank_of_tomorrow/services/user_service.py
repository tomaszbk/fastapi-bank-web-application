from sqlalchemy.orm import Session

from datetime import datetime

from bank_of_tomorrow.infrastructure.models import User, BankAccount
from bank_of_tomorrow.api.schemas.user_schemas import UserCreate
from bank_of_tomorrow.services.auth_service import auth
from bank_of_tomorrow.domain.bank_account_logic import DEFAULT_FIRST_ACCOUNT_BALANCE


def user_already_exists(session: Session, username: str):
    return session.query(User).filter(User.username == username).one_or_none() is not None


def create_user(session: Session, form_data: UserCreate):
    hashed_password = auth.hash_password(form_data.password)
    now = datetime.now()
    user = User(
        username=form_data.username,
        hashed_password=hashed_password,
        email=form_data.email,
        dni=form_data.dni,
        age=form_data.age,
        name=form_data.name,
        surname=form_data.surname,
        creation_date=now,
        last_updated=now,
    )
    user.bank_account = BankAccount(balance=DEFAULT_FIRST_ACCOUNT_BALANCE, creation_date=now)
    session.add(user)
    session.commit()
    return user


def get_by_username(session: Session, username: str):
    user = session.query(User).filter_by(username=username).one_or_none()
    return user


def get_transactions(user: User):
    """Get all transactions from a user orderer by date"""
    transactions = user.bank_account.origin_transactions + user.bank_account.destiny_transactions
    transactions.sort(key=lambda transaction: transaction.transaction_date, reverse=True)
    return transactions
