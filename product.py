from uuid import uuid4
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    product_id = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(String)
    photo = Column(BLOB)
    location = Column(String)
    category = Column(String)
    product_rank = Column(Float)

    def __init__(self, product_name, quantity, description, photo, location, category, product_rank, product_id=None):
        self.name = product_name
        self.price = quantity
        self.quantity = quantity
        self.description = description
        self.photo = photo
        self.location = location
        self.category = category
        self.product_rank = product_rank
        self.product_id = product_id if product_id else str(uuid4())

    def __str__(self):
        return f"{self.name}, {self.quantity}, {self.description}, {self.photo}, {self.location}, {self.category}, {self.product_rank}, {self.product_id}"

def connect():
    """ Connect to the SQLite database with an absolute path using SQLAlchemy. """
    parent_path = Path().resolve()
    db_path = f'sqlite:///{parent_path}/products.db'
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)  # Ensure tables are created
    return engine

def save_product(product):
    """ Insert a new Product into the database using SQLAlchemy session. """
    engine = connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        session.add(product)
        session.commit()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

def main():
    product = Product("psalidi", 2, "Scissors", "image_data_here", "Warehouse 1", "Tools", 4.8)
    print('Starting database operations...')
    save_product(product)  # Save the Product to the database
    print('Product saved successfully')

if __name__ == "__main__":
    main()
