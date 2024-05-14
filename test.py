from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
import re
from pathlib import Path

Base = declarative_base()

# Database connection path setup
parent_path = Path().resolve()
db_path = f'sqlite:///{parent_path}/database.db'

# Regular expressions for validation
password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

# Engine creation function
def get_engine():
    engine = create_engine(db_path, echo=True)
    Base.metadata.create_all(engine)
    return engine

# Session maker
def get_session(engine):
    return sessionmaker(bind=engine)()

class User(Base):
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    location = Column(String, nullable=False)
    ranking = Column(Float, default=4.8)

    # Relationship to products
    products = relationship("Product", back_populates="user")

    def __init__(self, name, surname, email, password, location, ranking=4.8):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.location = location
        self.ranking = ranking



class Product(Base):
    __tablename__ = 'products'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    product_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(String)
    photo = Column(String)
    location = Column(String)
    category = Column(String)
    product_rank = Column(Float)

    # Relationship to user
    user = relationship("User", back_populates="products")

    def __init__(self, user_id, product_name, price, quantity, description='', photo='', location='', category='', product_rank=0.0):
        self.user_id = user_id
        self.product_name = product_name
        self.price = price
        self.quantity = quantity
        self.description = description
        self.photo = photo
        self.location = location
        self.category = category
        self.product_rank = product_rank

# Example use case
def main():
    engine = get_engine()
    session = get_session(engine)

    # Create a user
    user = User(name="John", surname="Doe", email="john.doe@example.com", password="S!ecurepa1ssword123", location="New York")
    session.add(user)
    session.commit()

    # Create a product linked to the user
    product = Product(user_id=user.id, product_name="Scissors", price=10, quantity=100)
    session.add(product)
    session.commit()

    print("User and product saved successfully.")

if __name__ == "__main__":
    main()
