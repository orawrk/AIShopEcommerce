"""
Order and OrderItem model definitions
"""

from sqlalchemy import Column, String, Float, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel
from .enums import OrderStatusEnum


class Order(BaseModel):
    """Order model"""
    __tablename__ = "orders"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PROCESSING, nullable=False)
    shipping_address = Column(String(500), nullable=True)
    payment_method = Column(String(50), nullable=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", lazy="dynamic", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Order(order_number='{self.order_number}', total={self.total_amount}, status='{self.status}')>"


class OrderItem(BaseModel):
    """Order item model"""
    __tablename__ = "order_items"
    
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem(order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"