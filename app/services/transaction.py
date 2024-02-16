from app.infrastructure.models import User, Transaction, bank_of_tomorrow
from app.infrastructure.external import (
    get_transaction_number,
    make_external_transaction,
)
from app.services.user import get_user_by_cbu
from app.services.account import handle_external_account, get_bank_account_by_cbu
from app.schemas.transaction import TransactionCreate

from sqlalchemy.orm import Session

from datetime import datetime
from sqlalchemy.exc import IntegrityError
from matplotlib import pyplot as plt

from io import BytesIO
import base64


def create_transaction(session: Session, data: TransactionCreate) -> None:
    date = datetime.now()
    if data.origin_cbu[:10] == bank_of_tomorrow.code:
        start_transaction(session, data, date)
    else:
        handle_incoming_transaction(session, data, date)


def get_transactions_chart(user: User, transactions: list[Transaction]):
    if len(transactions) == 0:
        return None
    amounts, dates = zip(
        *(
            (t.amount if t.origin_account_id != user.id else -t.amount, t.date)
            for t in transactions
        ),
        strict=True,
    )
    plt.bar(
        range(len(dates)),
        amounts,
        tick_label=[date.strftime("%Y-%m-%d") for date in dates],
    )
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Transaction Chart")
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    return plot_data


def start_transaction(session: Session, data: TransactionCreate, date) -> None:
    transaction_number = get_transaction_number()
    transaction = Transaction(transaction_number, data.amount, date)
    origin_user = get_user_by_cbu(session, data.origin_cbu)
    if not origin_user:
        raise Exception("No user found with origin cbu")
    origin_user.bank_account.balance -= data.amount
    session.add(origin_user.bank_account)
    try:
        session.flush()
    except IntegrityError as e:
        # implicit rollback
        raise Exception(f"User doesn't have enough money: {e}") from e
    if data.destiny_cbu[:10] == bank_of_tomorrow.code:
        destiny_user = get_user_by_cbu(session, data.destiny_cbu)
        if not destiny_user:
            raise Exception("No user found with destiny cbu")
        destiny_user.bank_account.balance += data.amount
        transaction.origin_account = origin_user.bank_account
        transaction.destination_account = destiny_user.bank_account
        session.add(transaction)
        session.commit()
        return
    else:
        destiny_account = handle_external_account(session, data.destiny_cbu)
        make_external_transaction(transaction, destiny_account, data.amount, data.motive)


def handle_incoming_transaction(session: Session, data: TransactionCreate, date: datetime) -> None:
    if data.number is None:
        raise Exception("Number is required for incoming transactions")
    destiny_account = get_bank_account_by_cbu(session, data.destiny_cbu)
    if not destiny_account:
        raise Exception("No user found with destiny cbu")

    origin_account = handle_external_account(session, data.origin_cbu)
    transaction = Transaction(data.number, data.amount, date)
    destiny_account.balance += data.amount
    transaction.destination_account = destiny_account
    transaction.origin_account = origin_account
    session.add(transaction)
    session.commit()
    origin_user = get_user_by_cbu(session, data.origin_cbu)
    if not origin_user:
        raise Exception("No user found with origin cbu")
