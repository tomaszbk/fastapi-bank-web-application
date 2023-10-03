from infrastructure.models import User
from entrypoints.api.schemas.user_schemas import UserLoginForm
from services.auth_service import auth
from sqlalchemy.orm import Session


def user_already_exists(session: Session, username: str):
    return session.query(User).filter(User.username == username).one_or_none() is not None


def create_user(session: Session, form_data: UserLoginForm):
    hashed_password = auth.get_hashed_password(form_data.password)
    user = User(
        username=form_data.username,
        hashed_password=hashed_password,
        email=form_data.email,
        dni=form_data.dni,
        age=form_data.age,
        name=form_data.name,
        surname=form_data.surname,
    )
    session.add(user)
    session.commit()
    return user
