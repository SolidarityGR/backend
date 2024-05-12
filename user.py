from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path

Base = declarative_base()

class User(Base):
    """
    A class to represent a user in a system, using SQLAlchemy for interacting with a SQLite database.

    Attributes:
        id (int): Unique identifier for the user.
        name (str): First name of the user.
        surname (str): Last name of the user.
        email (str): Email address of the user.
        password (str): Password for the user's account.
        location (str): The geographic location associated with the user.
        ranking (float): A numerical rating or ranking for the user, defaulting to 4.8.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    location = Column(String, nullable=False)
    ranking = Column(Float, default=4.8)

    def __init__(self, name, surname, email, password, location, ranking=4.8):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.location = location
        self.ranking = ranking

def connect():
    """ Connect to the SQLite database with an absolute path using SQLAlchemy. """
    parent_path = Path().resolve()
    db_path = f'sqlite:///{parent_path}/users.db'
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)  # Ensure tables are created
    return engine

def save_user(user):
    """ Insert a new user into the database using SQLAlchemy session. """
    engine = connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        session.add(user)
        session.commit()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

def update_user_email(user, new_email):
    """ Update the email address of the user in the database. """
    engine = connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        user.email = new_email
        session.commit()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

def update_user_password(user, new_password):
    """ Update the user's password in the database. """
    engine = connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        user.password = new_password
        session.commit()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

def main():
    user = User("John", "Doe", "john.doe@example.com", "securepassword123", "New York")
    save_user(user)  # Save the user to the database
    print('User saved successfully')

if __name__ == "__main__":
    main()
