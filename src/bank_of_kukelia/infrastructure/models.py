from sqlalchemy import  Integer, String, MetaData, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, MappedAsDataclass
from datetime import datetime

metadata = MetaData()


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('username', name='users_username_key')
    )

    id: Mapped[int] = mapped_column(Integer, init=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    dni: Mapped[int] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
 #   creation_date: Mapped[datetime] = mapped_column(datetime, nullable=False)
