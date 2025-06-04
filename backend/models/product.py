"""
Product model definition
"""

from sqlalchemy import Column, String, Float, Integer, Text, Enum
from sqlalchemy.orm import relationship
from models.base import BaseModel
from models.enums import ProductCategoryEnum


class Product(BaseModel):
    """Product model"""
    __tablename__ = "products"
    
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    category = Column(Enum(ProductCategoryEnum), nullable=False, index=True)
    stock_quantity = Column(Integer, default=0, nullable=False)
    rating = Column(Float, default=0.0, nullable=False)
    image_url = Column(String(500), nullable=True)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    # Relationships will be defined after all models are created
    
    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price}, category='{self.category}')>"