"""
Order controller for handling HTTP requests
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..config.database import get_database
from ..services.order_service import OrderService
from ..services.user_service import UserService
from ..schemas.order_schemas import (
    OrderCreateSchema,
    OrderUpdateSchema,
    OrderResponseSchema,
    OrderListResponseSchema
)
import math


class OrderController:
    """Order controller for API endpoints"""
    
    def __init__(self):
        self.router = APIRouter()
        self._register_routes()
    
    def _register_routes(self):
        """Register all order routes"""
        
        @self.router.post("/", response_model=OrderResponseSchema, status_code=status.HTTP_201_CREATED)
        async def create_order(
            order_data: OrderCreateSchema,
            current_user = Depends(UserService.get_current_user),
            db: Session = Depends(get_database)
        ):
            """Create a new order"""
            try:
                order = OrderService.create_order(db, current_user.id, order_data)
                return order
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to create order: {str(e)}"
                )
        
        @self.router.get("/", response_model=OrderListResponseSchema)
        async def get_user_orders(
            page: int = 1,
            page_size: int = 10,
            current_user = Depends(UserService.get_current_user),
            db: Session = Depends(get_database)
        ):
            """Get current user's orders"""
            orders, total_count = OrderService.get_user_orders(db, current_user.id, page, page_size)
            total_pages = math.ceil(total_count / page_size)
            
            return OrderListResponseSchema(
                orders=orders,
                total_count=total_count,
                page=page,
                page_size=page_size,
                total_pages=total_pages
            )
        
        @self.router.get("/{order_id}", response_model=OrderResponseSchema)
        async def get_order(
            order_id: int,
            current_user = Depends(UserService.get_current_user),
            db: Session = Depends(get_database)
        ):
            """Get order by ID"""
            order = OrderService.get_order_by_id(db, order_id)
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
            
            # Check if user owns the order or is admin
            if order.user_id != current_user.id and current_user.role.value != "admin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to view this order"
                )
            
            return order
        
        @self.router.put("/{order_id}", response_model=OrderResponseSchema)
        async def update_order(
            order_id: int,
            order_data: OrderUpdateSchema,
            current_user = Depends(UserService.get_current_user),
            db: Session = Depends(get_database)
        ):
            """Update order (admin only for status updates)"""
            if current_user.role.value != "admin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only admins can update orders"
                )
            
            order = OrderService.update_order(db, order_id, order_data)
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
            return order