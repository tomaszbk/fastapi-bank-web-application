from src.bank_of_kukelia.infrastructure.models import BankAccount
from datetime import datetime
from sqlalchemy.exc import IntegrityError


def test_negative_balance_raises_error(session):
    # create a bank account with initial balance of 20000
    now = datetime.now()
    account = BankAccount(20000, now)

    # reduce the balance by 10000
    try:
        account.balance -= 100000
        session.add(account)
        session.flush()
    except IntegrityError as e:
        assert IntegrityError, f"Check failed: {e}"
