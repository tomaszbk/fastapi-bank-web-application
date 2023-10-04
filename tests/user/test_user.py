import pytest

from services.user_service import user_already_exists, create_user
from entrypoints.api.schemas.user_schemas import UserLoginForm


def test_user_registration(session):
    form_data = UserLoginForm(
        username="test_username",
        password="test",
        name="test",
        surname="test",
        dni=12345678,
        age=18,
        email="test@hotmail.com",
    )
    user = create_user(session, form_data)
    assert user is not None
    assert user.username == "test_username"
    assert user_already_exists(session, "test_username") is True
