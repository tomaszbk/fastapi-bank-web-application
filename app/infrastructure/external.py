import json

import requests

from app.config import config
from app.infrastructure.models import BankAccount, Transaction


def get_transaction_number() -> str:
    """returns transaction number"""
    payload = {}
    json_payload = json.dumps(payload)
    response = requests.post(config["BROKER_URL"] + "/algo", json_payload)
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


def validate_identity():
    payload = {
        "clientId": "e9df95af-bfb9-4757-a5c8-ce02b44ceaeb",
        "clientSecret": "123",
        "authorizationCode ": "2tzfsgApkPrIB8MAqtjGOw6Bjyl83MIrySXcMyaU",
    }
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    json_payload = json.dumps(payload)
    response = requests.post(
        "https://colosal.duckdns.org:15001/Renaper/api/Auth/loguearJWT",
        json_payload,
        headers=headers,
        verify=False,
    )
    return response.json()
