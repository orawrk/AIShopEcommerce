"""
Cart model definition
"""

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class CartItem(BaseModel):
    """Cart item model"""
    __tablename__ = "cart_items"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    
    # Relationships
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")
    
    def __repr__(self):
        return f"<CartItem(user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity})>"