def test_create_transaction(session):
    from datetime import datetime

    from app.infrastructure.models import Account
    from app.services.transaction_service import create_transaction
    from tests.factories import user_factory

    user1 = user_factory()
    user1.bank_account = Account(balance=8000, creation_date=datetime.now())
    user2 = user_factory()
    user2.bank_account = Account(balance=1000, creation_date=datetime.now())
    amount = 5000
    create_transaction(session, user1, amount, user2)
    assert user1.bank_account.balance == 3000, "origin user balance error"
    assert user2.bank_account.balance == 6000, "destiny user balance error"
