from domain.models.models import User
from domain.ports.user_repository import UserRepository
from entrypoints.api.schemas.user_schemas import UserLoginForm
from services.auth_service import auth


def user_already_exists(user_repo: UserRepository, username: str):
    return user_repo.get_by_username(username) is not None


def create_user(user_repo: UserRepository, form_data: UserLoginForm):
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
    user_repo.add(user)
    return user
