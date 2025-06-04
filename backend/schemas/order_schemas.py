"""
Order-related Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from ..models.enums import OrderStatusEnum


class OrderItemSchema(BaseModel):
    """Order item schema"""
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    total_price: float = Field(..., gt=0)


class OrderItemResponseSchema(OrderItemSchema):
    """Order item response schema"""
    id: int
    order_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class OrderCreateSchema(BaseModel):
    """Order creation schema"""
    shipping_address: Optional[str] = None
    payment_method: Optional[str] = None
    items: List[OrderItemSchema]


class OrderUpdateSchema(BaseModel):
    """Order update schema"""
    status: Optional[OrderStatusEnum] = None
    shipping_address: Optional[str] = None


class OrderResponseSchema(BaseModel):
    """Order response schema"""
    id: int
    user_id: int
    total_amount: float
    status: OrderStatusEnum
    shipping_address: Optional[str]
    payment_method: Optional[str]
    order_number: str
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponseSchema] = []

    class Config:
        from_attributes = True


class OrderListResponseSchema(BaseModel):
    """Order list response schema"""
    orders: List[OrderResponseSchema]
    total_count: int
    page: int
    page_size: int
    total_pages: int