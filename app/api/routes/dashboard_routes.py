from fastapi import APIRouter, Depends, Request

from app.api.routes.auth_routes import (
    get_current_user_from_header,
    get_current_user_from_url,
)
from app.config import templates
from app.infrastructure.engine import postgres_session_factory
from app.infrastructure.models import User
from app.schemas.transaction import TransactionCreate, TransactionCreateFront
from app.schemas.user import UserRead
from app.services.transaction import create_transaction, get_transactions_chart

router = APIRouter()


@router.get("")
async def dashboard_view(request: Request, user: User = Depends(get_current_user_from_url)):
    """Template includes chart of user's balance over time,
    and a table of user's recent transactions."""
    transactions = (
        user.bank_account.origin_transactions + user.bank_account.destination_transactions
    )
    transactions.sort(key=lambda transaction: transaction.date, reverse=True)
    image = get_transactions_chart(user, transactions)
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user, "transactions": transactions, "image": image},
    )


@router.get("/profile")
async def profile_view(request: Request, user: UserRead = Depends(get_current_user_from_url)):
    """Template shows User data."""
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})


@router.get("/transaction")
async def transaction_view(request: Request, user: UserRead = Depends(get_current_user_from_url)):
    """Template allows to create a new transaction."""
    return templates.TemplateResponse("transaction.html", {"request": request, "user": user})


@router.post("/transaction")
async def transaction(
    transaction: TransactionCreate, session=Depends(postgres_session_factory.get_session)
):
    """Creates a new transaction."""
    create_transaction(session, transaction)
    return {"message": "Transaction created successfully"}


@router.post("/transaction-front")
async def transaction_front(
    transaction: TransactionCreateFront,
    session=Depends(postgres_session_factory.get_session),
    user: User = Depends(get_current_user_from_header),
):
    """Creates a new transaction."""
    data = TransactionCreate(
        origin_cbu=user.bank_account.cbu,
        amount=transaction.amount,
        destination_cbu=transaction.destination_cbu,
        motive=transaction.motive,
        number=transaction.number,
    )
    create_transaction(session, data)
    return {"message": "Transaction created successfully"}
