import requests

from app.config import config
from app.infrastructure.models import BankAccount, Transaction


def get_transaction_number() -> str:
    """returns transaction number"""

    response = requests.post(config["BROKER_URL"] + "/algo")
    if response.status_code != 200:
        raise Exception(f"Error starting transaction: {response.text}")
    return response.text


def make_external_transaction(
    transaction: Transaction,
    destination_account: BankAccount,
    amount: float,
    motive: str | None,
) -> None:
    """Sends a transaction to an external bank"""

    response = requests.post(
        destination_account.bank.url + "/transaction",
        json={
            "number": transaction.number,
            "origin_cbu": transaction.origin_account.cbu,
            "destination_cbu": destination_account.cbu,
            "amount": amount,
            "motive": motive,
        },
    )
    if response.status_code != 200:
        raise Exception(f"Error making external transaction: {response.text}")
