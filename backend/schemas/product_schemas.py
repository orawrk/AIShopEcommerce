"""
Product-related Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from ..models.enums import ProductCategoryEnum, ProductSortByEnum, SortOrderEnum


class ProductBaseSchema(BaseModel):
    """Base product schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category: ProductCategoryEnum
    stock_quantity: int = Field(..., ge=0)
    rating: float = Field(0.0, ge=0, le=5)
    image_url: Optional[str] = None
    sku: str = Field(..., min_length=1, max_length=100)


class ProductCreateSchema(ProductBaseSchema):
    """Product creation schema"""
    pass


class ProductUpdateSchema(BaseModel):
    """Product update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category: Optional[ProductCategoryEnum] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    rating: Optional[float] = Field(None, ge=0, le=5)
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class ProductResponseSchema(ProductBaseSchema):
    """Product response schema"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductListResponseSchema(BaseModel):
    """Product list response schema"""
    products: List[ProductResponseSchema]
    total_count: int
    page: int
    page_size: int
    total_pages: int


class ProductSearchSchema(BaseModel):
    """Product search schema"""
    search_term: Optional[str] = None
    category: Optional[ProductCategoryEnum] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    sort_by: ProductSortByEnum = ProductSortByEnum.NAME
    sort_order: SortOrderEnum = SortOrderEnum.ASC
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)