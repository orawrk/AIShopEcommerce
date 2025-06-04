"""
Product controller for handling HTTP requests
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from config.database import get_database
from services.product_service import ProductService
from schemas.product_schemas import (
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductResponseSchema,
    ProductListResponseSchema,
    ProductSearchSchema
)
import math


class ProductController:
    """Product controller for API endpoints"""
    
    def __init__(self):
        self.router = APIRouter()
        self._register_routes()
    
    def _register_routes(self):
        """Register all product routes"""
        
        @self.router.post("/", response_model=ProductResponseSchema, status_code=status.HTTP_201_CREATED)
        async def create_product(
            product_data: ProductCreateSchema,
            db: Session = Depends(get_database)
        ):
            """Create a new product"""
            try:
                product = ProductService.create_product(db, product_data)
                return product
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to create product: {str(e)}"
                )
        
        @self.router.get("/{product_id}", response_model=ProductResponseSchema)
        async def get_product(
            product_id: int,
            db: Session = Depends(get_database)
        ):
            """Get product by ID"""
            product = ProductService.get_product_by_id(db, product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found"
                )
            return product
        
        @self.router.get("/", response_model=ProductListResponseSchema)
        async def get_products(
            search_term: str = None,
            category: str = None,
            min_price: float = None,
            max_price: float = None,
            sort_by: str = "name",
            sort_order: str = "asc",
            page: int = 1,
            page_size: int = 10,
            db: Session = Depends(get_database)
        ):
            """Get products with search and filtering"""
            search_params = ProductSearchSchema(
                search_term=search_term,
                category=category,
                min_price=min_price,
                max_price=max_price,
                sort_by=sort_by,
                sort_order=sort_order,
                page=page,
                page_size=page_size
            )
            
            products, total_count = ProductService.get_products(db, search_params)
            total_pages = math.ceil(total_count / page_size)
            
            return ProductListResponseSchema(
                products=products,
                total_count=total_count,
                page=page,
                page_size=page_size,
                total_pages=total_pages
            )
        
        @self.router.put("/{product_id}", response_model=ProductResponseSchema)
        async def update_product(
            product_id: int,
            product_data: ProductUpdateSchema,
            db: Session = Depends(get_database)
        ):
            """Update product"""
            product = ProductService.update_product(db, product_id, product_data)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found"
                )
            return product
        
        @self.router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete_product(
            product_id: int,
            db: Session = Depends(get_database)
        ):
            """Delete product"""
            success = ProductService.delete_product(db, product_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found"
                )
        
        @self.router.patch("/{product_id}/stock", response_model=ProductResponseSchema)
        async def update_stock(
            product_id: int,
            quantity_change: int,
            db: Session = Depends(get_database)
        ):
            """Update product stock"""
            try:
                product = ProductService.update_stock(db, product_id, quantity_change)
                if not product:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Product not found"
                    )
                return product
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )