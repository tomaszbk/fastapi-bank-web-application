import base64
from datetime import datetime
from io import BytesIO

from matplotlib import pyplot as plt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.infrastructure.external import (
    # get_transaction_number,
    make_external_transaction,
)
from app.infrastructure.models import Transaction, User, bank_of_tomorrow
from app.schemas.transaction import TransactionCreate
from app.services.account import get_bank_account_by_cbu, handle_external_account


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
    # TODO
    # transaction_number = get_transaction_number()
    transaction_number = "1"
    transaction = Transaction(transaction_number, data.amount, date)
    origin_account = get_bank_account_by_cbu(session, data.origin_cbu)
    if not origin_account:
        raise Exception("No account found with origin cbu")
    origin_account.balance -= data.amount
    transaction.origin_account = origin_account
    session.add(origin_account)
    try:
        session.flush()
    except IntegrityError as e:
        # implicit rollback
        raise Exception(f"User doesn't have enough money: {e}") from e
    if data.destination_cbu[:10] == bank_of_tomorrow.code:
        destination_account = get_bank_account_by_cbu(session, data.destination_cbu)
        if not destination_account:
            raise Exception("No account found with destination cbu")
        destination_account.balance += data.amount
        transaction.destination_account = destination_account
        session.add(transaction)
        session.commit()
        return
    else:
        destination_account = handle_external_account(session, data.destination_cbu)
        make_external_transaction(transaction, destination_account, data.amount, data.motive)
        session.add(transaction)
        session.commit()


def handle_incoming_transaction(session: Session, data: TransactionCreate, date: datetime) -> None:
    if data.number is None:
        raise Exception("Number is required for incoming transactions")
    destination_account = get_bank_account_by_cbu(session, data.destination_cbu)
    if not destination_account:
        raise Exception("No user found with destination cbu")

    origin_account = handle_external_account(session, data.origin_cbu)
    transaction = Transaction(data.number, data.amount, date)
    destination_account.balance += data.amount
    transaction.destination_account = destination_account
    transaction.origin_account = origin_account
    session.add(transaction)
    session.commit()
