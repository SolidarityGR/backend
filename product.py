from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from uuid import uuid4
from base import Base

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
