from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.session import sessionmaker
from loguru import logger

from config import get_postgres_uri


class PostgresSessionFactory:
    def __init__(self) -> None:
        self.engine = create_engine(get_postgres_uri())
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        session = self.Session()
        try:
            logger.info("session created")
            yield session
        finally:
            logger.info("session closed")
            session.close()


class PostgresLocalSessionFactory:
    def __init__(self) -> None:
        self.engine = create_engine(get_postgres_uri())
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()


postgres_session_factory = PostgresSessionFactory()
postgres_local_session_factory = PostgresLocalSessionFactory()
