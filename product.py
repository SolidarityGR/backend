from uuid import uuid4
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path
import re, json

Base = declarative_base()

parent_path = Path().resolve()
db_path = f'sqlite:///{parent_path}/database.db'


class Product(Base):
    __tablename__ = 'products'

    id = Column(String(36), primary_key=True, unique=True, nullable=False, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    product_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(String)
    photo = Column(String)
    location = Column(String)
    category = Column(String)
    product_rank = Column(Float)
    

    def __init__(self, product_name, user_id, quantity, description, photo, location, category, product_rank):
        assert isinstance(product_name, str), "Product name must be a string"
        assert isinstance(user_id, str), "User ID must be a string"
        assert isinstance(quantity, int), "Quantity must be an integer"
        assert isinstance(description, str), "Description must be a string"
        assert isinstance(photo, str), "Photo must be a BLOB"
        assert isinstance(location, str), "Location must be a string"
        assert isinstance(category, str), "Category must be a string"
        assert isinstance(product_rank, float), "Product rank must be a float"
        
        self.product_name = product_name 
        self.user_id = user_id
        self.price = quantity
        self.quantity = quantity
        self.description = description
        self.photo = photo
        self.category = category


    def connect(self):
        """ Connect to the SQLite database with an absolute path using SQLAlchemy. """
        print(db_path)
        engine = create_engine(db_path, echo=True)
        Base.metadata.create_all(engine)  # Ensure tables are created
        return engine

    def add_product(self):
        """ Insert a new Product into the database using SQLAlchemy session. """
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
            
    def get_product_by_id(self, product_id):
        """ Retrieve a Product from the database by its unique identifier. """
        engine = self.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            product = session.query(Product).filter_by(product_id=product_id).first()
        except SQLAlchemyError as e:
            print(f"Error: {e}")
        finally:
            session.close()
        return product

    def get_product_by_user_id(self, user_id):
        """ Retrieve a Product from the database by its unique identifier. """
        engine = self.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            product = session.query(Product).filter_by(user_id=user_id).all()
        except SQLAlchemyError as e:
            print(f"Error: {e}")
        finally:
            session.close()
        return product


    def update_product(self, product_id, new_product):
        """ Update the Product in the database from json."""
        engine = self.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            product = session.query(Product).filter_by(product_id=product_id).first()
            product.product_name = new_product['product_name'] if 'product_name' in new_product and isinstance(new_product['product_name'], str) else product.product_name
            product.price = new_product['price'] if 'price' in new_product and isinstance(new_product['price'], int) else product.price
            product.quantity = new_product['quantity'] if 'quantity' in new_product and isinstance(new_product['quantity'], int) else product.quantity
            product.description = new_product['description'] if 'description' in new_product and isinstance(new_product['description'], str) else product.description
            product.photo = new_product['photo'] if 'photo' in new_product and isinstance(new_product['photo'], BLOB) else product.photo 
            product.location = new_product['location'] if 'location' in new_product and isinstance(new_product['location'], str) else product.location
            product.category = new_product['category'] if 'category' in new_product and isinstance(new_product['category'], str) else product.category
            product.product_rank = new_product['product_rank'] if 'product_rank' in new_product and isinstance(new_product['product_rank'], float) else product.product_rank
            session.commit()
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            session.rollback()
        finally:
            session.close()
        
        

# def main():
#     product = Product("psalidi", 2, "Scissors", "image_data_here", "Warehouse 1", "Tools", 4.8)
#     print('Starting database operations...')
#     product.add_product(product)  # Save the Product to the database
#     print('Product saved successfully')

# if __name__ == "__main__":
#     main()
