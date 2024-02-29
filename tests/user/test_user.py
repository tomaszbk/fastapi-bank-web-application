def test_user_registration(session):
    from app.schemas.user import UserCreate
    from app.services.user import create_user, user_already_exists

    form_data = UserCreate(
        username="test_username",
        password="test",
        name="test",
        surname="test",
        cuil=20123456782,
        age=18,
        email="test@hotmail.com",
    )
    user = create_user(session, form_data)
    assert user is not None
    assert user.username == "test_username"
    assert user_already_exists(session, "test_username") is True
    assert user.bank_account.balance == 10000


def test_external_user_registration(session):
    from app.services.user import get_user_by_username, handle_external_user

    code = "uoqb6lwP2uyAGx1WPQaXfkNW1ZZ1uYCpAeTOM7iT"
    jwt = handle_external_user(session, code)
    user = get_user_by_username(session, "aa")
    assert jwt is not None
    assert user is not None
