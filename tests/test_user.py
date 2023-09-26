import pytest

from services.user_service import user_already_exists, create_user
from api.schemas.user_schemas import UserLoginForm
from .test_repositories.fake_user_repo import FakeUserRepository


# Define a fixture to create a common variable
@pytest.fixture
def fake_user_repo():
    # You can initialize the common variable here
    fake_user_repo = FakeUserRepository()
    yield fake_user_repo


def test_user_registration(fake_user_repo):
    form_data = UserLoginForm(
        username="test_username",
        password="test",
        name="test",
        surname="test",
        dni=12345678,
        age=18,
        email="test@hotmail.com",
    )
    user = create_user(fake_user_repo, form_data)
    assert user is not None
    assert user.username == "test_username"
    assert user_already_exists(fake_user_repo, "test_username") is True
