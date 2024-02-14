from sqlalchemy.orm import Session

from datetime import datetime

from app.infrastructure.models import User, BankAccount, Bank, bank_of_tomorrow
from app.api.schemas.user_schemas import UserCreate
from app.services.auth_service import auth
from app.config import config


def user_already_exists(session: Session, username: str):
    return session.query(User).filter(User.username == username).one_or_none() is not None


def create_user(session: Session, form_data: UserCreate):
    hashed_password = auth.hash_password(form_data.password)
    now = datetime.now()
    user = User(
        username=form_data.username,
        hashed_password=hashed_password,
        email=form_data.email,
        cuit=form_data.cuit,
        age=form_data.age,
        name=form_data.name,
        surname=form_data.surname,
        creation_date=now,
        last_updated=now,
    )
    user.bank_account = create_bank_account(session, None)

    user.bank_account.cbu = bank_of_tomorrow.code + str(user.bank_account.id * 100000000000)
    session.add(user)
    session.commit()
    return user


def get_user_by_username(session: Session, username: str):
    user = session.query(User).filter_by(username=username).one_or_none()
    return user


def get_user_by_cbu(session: Session, cbu: str):
    bank_account = session.query(BankAccount).filter_by(cbu=cbu).one_or_none()
    return bank_account.user if bank_account else None


def create_bank_account(session: Session, cbu: str | None):
    date = datetime.now()
    bank_account = BankAccount(balance=config["DEFAULT_FIRST_ACCOUNT_BALANCE"], creation_date=date)
    if cbu:
        bank = session.query(Bank).filter_by(code=cbu[:10]).one_or_none()
        if bank:
            bank_account.bank = bank
        else:
            raise Exception("Bank not found")
        bank_account.cbu = cbu
    else:
        bank_account.bank = bank_of_tomorrow
        session.flush()
        bank_account.cbu = bank_of_tomorrow.code + str(bank_account.id * 100000000000)
    return bank_account
