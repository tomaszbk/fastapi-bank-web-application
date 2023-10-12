from datetime import datetime


def test_create_transaction(session):
    from tests.factories import user_factory
    from bank_of_tomorrow.services.transaction_service import create_transaction
    from bank_of_tomorrow.infrastructure.models import BankAccount

    user1 = user_factory()
    user1.bank_account = BankAccount(balance=8000, creation_date=datetime.now())
    user2 = user_factory()
    user2.bank_account = BankAccount(balance=1000, creation_date=datetime.now())
    amount = 5000
    create_transaction(session, user1, amount, user2)
    assert user1.bank_account.balance == 3000, "origin user balance error"
    assert user2.bank_account.balance == 6000, "destiny user balance error"
