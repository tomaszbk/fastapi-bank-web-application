from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:postgres@desarrollo-postgres-1:5432/postgres')

# session factory
Session = sessionmaker(bind=engine)

class User():
    id: int

def get_session():
    return Session()
