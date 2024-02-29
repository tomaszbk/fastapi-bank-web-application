from datetime import datetime

from sqlalchemy.orm import Session

from app.infrastructure.models import BankAccount, User, bank_of_tomorrow
from app.schemas.user import UserCreate
from app.services.account import create_bank_account
from app.services.auth import auth


def user_already_exists(session: Session, username: str):
    return session.query(User).filter(User.username == username).one_or_none() is not None


def create_user(session: Session, form_data: UserCreate):
    hashed_password = auth.hash_password(form_data.password)
    now = datetime.now()
    user = User(
        username=form_data.username,
        hashed_password=hashed_password,
        email=form_data.email,
        cuil=form_data.cuil,
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


def handle_external_user(session: Session, access_code: str) -> str:
    jwt, data = auth.handle_external_login(access_code)
    username = data["Nombre"] + data["Apellido"]
    if user_already_exists(session, username):
        return jwt
    user_data = UserCreate(
        name=data["Nombre"],
        surname=data["Apellido"],
        email=data["Email"],
        cuil=data["Cuil"],
        username=username,
        password="RENAPER",
        age=18,
    )
    create_user(session=session, form_data=user_data)
    return jwt
