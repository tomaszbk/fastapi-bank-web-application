from sqlalchemy.engine.create import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker, mapper, registry
from domain.models.models import User

engine = create_engine('postgresql://postgres:postgres@desarrollotp-postgres-1:5432/postgres')

# session factory
Session = sessionmaker(bind=engine)
metadata = MetaData()


users_table = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(50), nullable=False),
    Column('name', String(50), nullable=False),
    Column('surname', String(50), nullable=False),
    Column('hashed_password', String(50), nullable=False),
    Column('email', String(50), nullable=False),
    Column('dni', String(50), nullable=False),
    Column('age', Integer, nullable=False)
)

def get_session():
    return Session()

def start_mappers():
    mapper_registry = registry()
    mapper_registry.map_imperatively(User, users_table)
