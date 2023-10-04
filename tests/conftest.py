import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.bank_of_kukelia.infrastructure.models import Base
import os


@pytest.fixture(scope="session")
def session():
    engine = create_engine('sqlite:///tests/test.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
