def test_user_registration(session):
    from app.services.user_service import user_already_exists, create_user
    from app.api.schemas.user_schemas import UserCreate

    form_data = UserCreate(
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
    assert user.bank_account.balance == 10000
