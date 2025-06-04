"""
Cart controller for handling HTTP requests
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..config.database import get_database
from ..services.cart_service import CartService
from ..services.user_service import UserService
from ..schemas.cart_schemas import (
    CartItemCreateSchema,
    CartItemUpdateSchema,
    CartItemResponseSchema
)


class CartController:
    """Cart controller for API endpoints"""
    
    def __init__(self):
        self.router = APIRouter()
        self._register_routes()
    
    def _register_routes(self):
        """Register all cart routes"""
        
        @self.router.post("/items", response_model=CartItemResponseSchema, status_code=status.HTTP_201_CREATED)
        async def add_to_cart(
            item_data: CartItemCreateSchema,
            current_user = Depends(UserService.get_current_user),
            db: Session = Depends(get_database)
        ):
            """Add item to cart"""
            try:
                cart_item = CartService.add_to_cart(db, current_user.id, item_data)
                return cart_item
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )
        
        @self.router.get("/items", response_model=List[CartItemResponseSchema])
        async def get_cart_items(
            current_user = Depends(UserService.get_current_user),
            db: Session = Depends(get_database)
        ):
            """Get current user's cart items"""
            return CartService.get_cart_items(db, current_user.id)
        
        @self.router.put("/items/{item_id}", response_model=CartItemResponseSchema)
        async def update_cart_item(
            item_id: int,
            item_data: CartItemUpdateSchema,
            current_user = Depends(UserService.get_current_user),
            db: Session = Depends(get_database)
        ):
            """Update cart item quantity"""
            cart_item = CartService.update_cart_item(db, current_user.id, item_id, item_data)
            if not cart_item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cart item not found"
                )
            return cart_item
        
        @self.router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
        async def remove_from_cart(
            item_id: int,
            current_user = Depends(UserService.get_current_user),
            db: Session = Depends(get_database)
        ):
            """Remove item from cart"""
            success = CartService.remove_from_cart(db, current_user.id, item_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cart item not found"
                )
        
        @self.router.delete("/clear", status_code=status.HTTP_204_NO_CONTENT)
        async def clear_cart(
            current_user = Depends(UserService.get_current_user),
            db: Session = Depends(get_database)
        ):
            """Clear all items from cart"""
            CartService.clear_cart(db, current_user.id)