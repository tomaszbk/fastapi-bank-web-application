from matplotlib import pyplot as plt
from io import BytesIO
import base64

from bank_of_tomorrow.infrastructure.models import User, Transaction


def create_transactions_chart(user: User, transactions: list[Transaction]):
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
