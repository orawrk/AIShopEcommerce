"""
Cart-related Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from datetime import datetime
from .product_schemas import ProductResponseSchema


class CartItemBaseSchema(BaseModel):
    """Base cart item schema"""
    product_id: int
    quantity: int = Field(..., gt=0)


class CartItemCreateSchema(CartItemBaseSchema):
    """Cart item creation schema"""
    pass


class CartItemUpdateSchema(BaseModel):
    """Cart item update schema"""
    quantity: int = Field(..., ge=0)


class CartItemResponseSchema(CartItemBaseSchema):
    """Cart item response schema"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    product: ProductResponseSchema = None

    class Config:
        from_attributes = True