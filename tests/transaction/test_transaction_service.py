from src.bank_of_kukelia.services.transaction_service import create_transaction
from src.bank_of_kukelia.infrastructure.models import BankAccount
from datetime import datetime
from factories import user_factory

def test_create_transaction(session):
    user1 = user_factory()
    user1.bank_account = BankAccount(balance=8000, creation_date=datetime.now())
    user2 = user_factory()
    user2.bank_account = BankAccount(balance=1000, creation_date=datetime.now())
    amount = 5000
    create_transaction(session, user1, amount, user2)
    assert user1.bank_account.balance == 3000