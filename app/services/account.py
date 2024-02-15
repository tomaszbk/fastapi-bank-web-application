from sqlalchemy.orm import Session

from datetime import datetime

from app.infrastructure.models import BankAccount, Bank, bank_of_tomorrow

from app.config import config


def get_bank_account_by_cbu(session: Session, cbu: str):
    return session.query(BankAccount).filter_by(cbu=cbu).one_or_none()


def create_bank_account(session: Session, cbu: str | None):
    date = datetime.now()
    bank_account = BankAccount(balance=config["DEFAULT_FIRST_ACCOUNT_BALANCE"], creation_date=date)
    if cbu:
        bank = session.query(Bank).filter_by(code=cbu[:10]).one_or_none()
        if bank:
            bank_account.bank = bank
        else:
            raise Exception("Bank not found")
        bank_account.cbu = cbu
    else:
        bank_account.bank = bank_of_tomorrow
        session.flush()
        bank_account.cbu = bank_of_tomorrow.code + str(bank_account.id * 100000000000)
    return bank_account


def handle_external_account(session: Session, cbu: str):
    account = get_bank_account_by_cbu(session, cbu)
    if not account:
        account = create_bank_account(session, cbu)
    return account
