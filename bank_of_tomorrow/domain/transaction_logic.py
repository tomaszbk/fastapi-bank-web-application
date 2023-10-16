from matplotlib import pyplot as plt
from io import BytesIO
import base64
from loguru import logger

from bank_of_tomorrow.infrastructure.models import User, Transaction
from bank_of_tomorrow.infrastructure.redis_client import redis_client_factory


async def get_transactions_chart(
    user: User, transactions: list[Transaction], cache=redis_client_factory.get_client()
):
    if await cache.exists(user.username):
        logger.info("getting chart from cache")
        return await cache.get(user.id)
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
    await cache.set(user.username, plot_data)
    return plot_data
