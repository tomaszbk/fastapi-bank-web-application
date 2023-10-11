"""initial migration

Revision ID: 00b53d3b7ba0
Revises:
Create Date: 2023-10-11 20:46:41.235570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "00b53d3b7ba0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("surname", sa.String(length=50), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("dni", sa.String(length=50), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("creation_date", sa.DateTime(), nullable=False),
        sa.Column("last_updated", sa.DateTime(), nullable=False),
        sa.Column("last_login", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
        sa.UniqueConstraint("username", name="users_username_key"),
    )
    op.create_table(
        "bank_accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("balance", sa.Double(precision=53), nullable=False),
        sa.Column("creation_date", sa.DateTime(), nullable=False),
        sa.CheckConstraint("balance >= 0.0", name="bank_accounts_balance_check"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="bank_accounts_user_id_fkey"),
        sa.PrimaryKeyConstraint("id", name="bank_accounts_pkey"),
        sa.UniqueConstraint("user_id", name="bank_accounts_user_id_key"),
    )
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("origin_account_id", sa.Integer(), nullable=False),
        sa.Column("destination_account_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Double(precision=53), nullable=False),
        sa.Column("transaction_date", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["destination_account_id"],
            ["bank_accounts.id"],
            name="transactions_destination_account_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["origin_account_id"], ["bank_accounts.id"], name="transactions_origin_account_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="transactions_pkey"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transactions")
    op.drop_table("bank_accounts")
    op.drop_table("users")
    # ### end Alembic commands ###
