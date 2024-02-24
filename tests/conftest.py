import pytest
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="session")
def session():
    from app.infrastructure.models import metadata

    logger.info("Creating test database")
    engine = create_engine("sqlite:///tests/test.db")
    metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    metadata.drop_all(engine)
