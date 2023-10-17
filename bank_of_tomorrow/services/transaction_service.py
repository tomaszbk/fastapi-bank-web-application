from bank_of_tomorrow.infrastructure.models import User, Transaction
from bank_of_tomorrow.domain.transaction_logic import create_transactions_chart
from bank_of_tomorrow.services.user_service import get_transactions as get_user_transactions
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime


def create_transaction(session: Session, origin_user: User, amount: float, destiny_user: User):
    now = datetime.now()
    transaction = Transaction(amount, now)
    origin_user.bank_account.balance -= amount
    session.add(origin_user.bank_account)
    try:
        session.flush()
    except IntegrityError as e:
        # implicit rollback
        raise Exception(f"User doesn't have enough money: {e}") from e
    destiny_user.bank_account.balance += amount
    transaction.origin_account = origin_user.bank_account
    transaction.destination_account = destiny_user.bank_account
    session.add(transaction)
    session.commit()
    return transaction


async def get_transactions_chart(user: User):
    transactions = get_user_transactions(user)
    return create_transactions_chart(user, transactions)
