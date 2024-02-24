from loguru import logger
from sqlmodel import Session, create_engine

from app.config import get_postgres_uri


class PostgresSessionFactory:
    def __init__(self) -> None:
        self.engine = create_engine(get_postgres_uri())
        self.Session = Session(self.engine)

    def get_session(self):
        session = self.Session()
        try:
            logger.info("session created")
            yield session
        finally:
            logger.info("session closed")
            session.close()

    def get_session_no_yield(self):
        return self.Session()


postgres_session_factory = PostgresSessionFactory()
