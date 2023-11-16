from app.infrastructure.models import User, Transaction

from sqlalchemy.orm import Session

from datetime import datetime
from sqlalchemy.exc import IntegrityError
from matplotlib import pyplot as plt

from io import BytesIO
import base64


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


def get_transactions_chart(user: User, transactions: list[Transaction]):
    if len(transactions) == 0:
        return None
    amounts, dates = zip(
        *(
            (t.amount if t.origin_account_id != user.id else -t.amount, t.transaction_date)
            for t in transactions
        ),
        strict=True,
    )
    plt.bar(range(len(dates)), amounts, tick_label=[date.strftime("%Y-%m-%d") for date in dates])
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Transaction Chart")
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    return plot_data
