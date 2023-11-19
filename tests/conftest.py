import pytest
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infrastructure.models import Base


@pytest.fixture(scope="session")
def session():
    logger.info("Creating test database")
    engine = create_engine("sqlite:///tests/test.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
