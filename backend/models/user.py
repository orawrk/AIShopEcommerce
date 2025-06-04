"""
User model definition
"""

from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel
from .enums import UserRoleEnum


class User(BaseModel):
    """User model"""
    __tablename__ = "users"
    
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.CUSTOMER, nullable=False)
    
    # Relationships
    orders = relationship("Order", back_populates="user", lazy="dynamic")
    cart_items = relationship("CartItem", back_populates="user", lazy="dynamic")
    user_behaviors = relationship("UserBehavior", back_populates="user", lazy="dynamic")
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"