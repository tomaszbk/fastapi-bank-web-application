import pytest
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="session")
def session():
    from app.infrastructure.models import Base, init_db

    logger.info("Creating test database")
    engine = create_engine("sqlite:///tests/test.db")
    init_db(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
