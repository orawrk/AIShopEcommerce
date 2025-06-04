"""
User behavior model for ML analytics
"""

from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class UserBehavior(BaseModel):
    """User behavior tracking model for ML analytics"""
    __tablename__ = "user_behaviors"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True, index=True)
    action = Column(String(50), nullable=False, index=True)  # view, add_to_cart, purchase, etc.
    session_duration = Column(Float, nullable=True)
    page_views = Column(Integer, default=1, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="user_behaviors")
    product = relationship("Product", back_populates="user_behaviors")
    
    def __repr__(self):
        return f"<UserBehavior(user_id={self.user_id}, action='{self.action}', product_id={self.product_id})>"