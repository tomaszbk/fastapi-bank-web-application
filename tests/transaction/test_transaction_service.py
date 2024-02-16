def test_create_transaction(session):
    from app.schemas.transaction import TransactionCreate
    from app.services.account import create_bank_account
    from app.services.transaction import create_transaction
    from tests.factories import user_factory

    user1 = user_factory()
    user1.bank_account = create_bank_account(session, cbu=None, balance=8000)
    user2 = user_factory()
    user2.bank_account = create_bank_account(session=session, cbu=None, balance=1000)
    amount = 5000
    data = TransactionCreate(
        origin_cbu=user1.bank_account.cbu, destination_cbu=user2.bank_account.cbu, amount=amount
    )
    create_transaction(session, data)
    assert user1.bank_account.balance == 3000, "origin user balance error"
    assert user2.bank_account.balance == 6000, "destination user balance error"
