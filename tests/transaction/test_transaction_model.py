def test_negative_balance_raises_error(session):
    from datetime import datetime

    from sqlalchemy.exc import IntegrityError

    from app.infrastructure.models import Account

    # create a bank account with initial balance of 20000
    now = datetime.now()
    account = Account(balance=20000, creation_date=now)

    try:
        account.balance -= 100000
        session.add(account)
        session.flush()
    except IntegrityError as e:
        session.rollback()
        assert IntegrityError, f"Check failed: {e}"
