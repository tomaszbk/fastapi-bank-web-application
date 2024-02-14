from fastapi import APIRouter, Request, HTTPException, status, Depends

from app.api.routes.auth_routes import (
    get_current_user_from_header,
    get_current_user_from_url,
)
from app.api.schemas.user_schemas import UserRead
from app.api.schemas.transaction_schemas import TransactionCreate

from app.services.transaction_service import create_transaction, get_transactions_chart
from app.services.user_service import get_user_by_cbu, create_bank_account

from app.infrastructure.engine import postgres_session_factory
from app.infrastructure.models import User, bank_of_tomorrow
from app.config import templates

router = APIRouter()


@router.get("")
async def dashboard_view(request: Request, user: User = Depends(get_current_user_from_url)):
    """Template includes chart of user's balance over time,
    and a table of user's recent transactions."""
    transactions = user.bank_account.origin_transactions + user.bank_account.destiny_transactions
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
    transaction: TransactionCreate,
    session=Depends(postgres_session_factory.get_session),
    user=Depends(get_current_user_from_header),
):
    """Creates a new transaction."""
    destiny_user = get_user_by_cbu(session, transaction.destiny_cbu)
    if destiny_user is None:
        if transaction.destiny_cbu[:10] != bank_of_tomorrow.code:
            create_bank_account(session, transaction.destiny_cbu)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No user found with provided username",
            )
    create_transaction(session, user, transaction.amount, destiny_user)
    return {"message": "Transaction created successfully"}
