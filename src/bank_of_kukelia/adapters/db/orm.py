from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://username:password@hostname:port/database')

# session factory
Session = sessionmaker(bind=engine)

def get_session():
    return Session()
