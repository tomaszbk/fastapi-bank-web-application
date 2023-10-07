from infrastructure.models import User, BankAccount, Transaction
from services.auth_service import auth

from domain.bank_account_logic import DEFAULT_FIRST_ACCOUNT_BALANCE
from sqlalchemy.orm import Session

from datetime import datetime
from sqlalchemy.exc import IntegrityError

def create_transaction(session: Session, origin_user: User, amount: float, destiny_user: User):

    now = datetime.now()
    transaction = Transaction(
        amount,
        now
    )
    origin_user.bank_account.balance -= amount
    session.add(origin_user.bank_account)
    try:
        session.flush()
    except IntegrityError as e:
        session.rollback()
        raise Exception( f"User doesn't have enough money: {e}") from e
    destiny_user.bank_account.balance += amount
    transaction.origin_account = origin_user.bank_account
    transaction.destination_account = destiny_user.bank_account
    session.add(transaction)
    session.commit()
    return transaction
