from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import re

Base = declarative_base()

# Database connection path setup
parent_path = Path().resolve()
db_path = f'sqlite:///{parent_path}/database.db'


# Engine creation function
def get_engine():
    engine = create_engine(db_path, echo=True)
    Base.metadata.create_all(engine)
    return engine

# Session maker
def get_session(engine):
    return sessionmaker(bind=engine)()
