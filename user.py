from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
import re
from pathlib import Path
from product import Product

Base = declarative_base()

parent_path = Path().resolve()
db_path = f'sqlite:///{parent_path}/database.db'

password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

product = Product

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

    id = Column(String(36), primary_key=True, unique=True, nullable=False, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    location = Column(String, nullable=False)
    ranking = Column(Float, default=4.8)

    def __init__(self, name, surname, email, password, location, ranking=4.8):
        assert isinstance(ranking, float), "Ranking must be a float"
        assert isinstance(name, str), "Name must be a string"
        assert isinstance(surname, str), "Surname must be a string"
        assert email_regex.match(email), "Email must be a valid email address"
        assert isinstance(password, str), "Password must be a string"
        assert password_regex.match(password), "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character"
        assert isinstance(location, str), "Location must be a string"
        
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.location = location
        self.ranking = ranking

    def connect(self):
        """ Connect to the SQLite database with an absolute path using SQLAlchemy. """
        engine = create_engine(db_path, echo=True)
        Base.metadata.create_all(engine)  # Ensure tables are created
        return engine

    def get_user_by_email(self, email):
        """ Retrieve a user from the database by their email address. """
        engine = self.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            user = session.query(User).filter_by(email=email).first()
        except SQLAlchemyError as e:
            print(f"Error: {e}")
        finally:
            session.close()
        return user

    def get_user_by_id(self, user_id):
        """ Retrieve a user from the database by their unique identifier. """
        
        engine = self.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            user = session.query(User).filter_by(user_id=user_id).first()
        except SQLAlchemyError as e:
            print(f"Error: {e}")
        finally:
            session.close()
        return user

    def add_user(self):
        """ Insert a new user into the database using SQLAlchemy session. """
        engine = self.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            session.add(self)
            session.commit()
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            session.rollback()
        finally:
            session.close()

    def update_user_email(self, user, new_email):
        """ Update the email address of the user in the database. """
        assert email_regex.match(new_email), "Email must be a valid email address"
        engine = self.connect()
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

    def update_user_password(self, user, new_password):
        """ Update the user's password in the database. """
        assert password_regex.match(new_password), "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character"
        engine = self.connect()
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


    def update_user_location(self, user, location):
        """ Update the location address of the user in the database. """
        assert isinstance(location, str), "Location must be a string"
        
        engine = self.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            user.location = location
            session.commit()
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            session.rollback()
        finally:
            session.close()
            
    def update_user_ranking(self, user, ranking):
        """ Update the ranking of the user in the database. """
        assert isinstance(ranking, float), "Ranking must be a float"
        engine = self.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            user.ranking = ranking
            session.commit()
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            session.rollback()
        finally:
            session.close()


def main():
    user = User("Joh1n", "Doe1", "john.d1oe@example.com", "S!ecurepa1ssword123", "New1York")
    user.add_user()  # Save the user to the database
    print('User saved successfully')

if __name__ == "__main__":
    main()
