from sqlalchemy.orm import Session

from datetime import datetime

from app.infrastructure.models import User, BankAccount
from app.api.schemas.user_schemas import UserCreate
from app.services.auth_service import auth
from app.domain.bank_account_logic import DEFAULT_FIRST_ACCOUNT_BALANCE


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
