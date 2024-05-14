from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from uuid import uuid4
from base import Base

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



