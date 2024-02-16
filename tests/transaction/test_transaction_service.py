def test_create_transaction(session):
    from datetime import datetime

    from app.infrastructure.models import BankAccount
    from app.schemas.transaction import TransactionCreate
    from app.services.transaction import create_transaction
    from tests.factories import user_factory

    user1 = user_factory()
    user1.bank_account = BankAccount(balance=8000, creation_date=datetime.now())
    user2 = user_factory()
    user2.bank_account = BankAccount(balance=1000, creation_date=datetime.now())
    amount = 5000
    data = TransactionCreate(
        origin_cbu=user1.bank_account.cbu, destiny_cbu=user2.bank_account.cbu, amount=amount
    )
    create_transaction(session, data)
    assert user1.bank_account.balance == 3000, "origin user balance error"
    assert user2.bank_account.balance == 6000, "destiny user balance error"
