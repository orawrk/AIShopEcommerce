"""
Order service layer for business logic
"""

from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..models.order import Order, OrderItem
from ..models.product import Product
from ..schemas.order_schemas import OrderCreateSchema, OrderUpdateSchema
import uuid
from datetime import datetime


class OrderService:
    """Order service for business logic operations"""
    
    @staticmethod
    def create_order(db: Session, user_id: int, order_data: OrderCreateSchema) -> Order:
        """Create a new order"""
        # Calculate total amount and validate items
        total_amount = 0.0
        order_items_data = []
        
        for item in order_data.items:
            # Verify product exists and has sufficient stock
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise ValueError(f"Product with ID {item.product_id} not found")
            
            if product.stock_quantity < item.quantity:
                raise ValueError(f"Insufficient stock for product {product.name}")
            
            item_total = product.price * item.quantity
            total_amount += item_total
            
            order_items_data.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": product.price,
                "total_price": item_total
            })
        
        # Generate unique order number
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
        
        # Create order
        db_order = Order(
            user_id=user_id,
            total_amount=total_amount,
            shipping_address=order_data.shipping_address,
            payment_method=order_data.payment_method,
            order_number=order_number
        )
        db.add(db_order)
        db.flush()  # To get the order ID
        
        # Create order items and update stock
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=db_order.id,
                **item_data
            )
            db.add(order_item)
            
            # Update product stock
            product = db.query(Product).filter(Product.id == item_data["product_id"]).first()
            product.stock_quantity -= item_data["quantity"]
        
        db.commit()
        db.refresh(db_order)
        return db_order
    
    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> Optional[Order]:
        """Get order by ID with items"""
        return db.query(Order).filter(Order.id == order_id).first()
    
    @staticmethod
    def get_user_orders(db: Session, user_id: int, page: int = 1, page_size: int = 10) -> Tuple[List[Order], int]:
        """Get user orders with pagination"""
        query = db.query(Order).filter(Order.user_id == user_id).order_by(desc(Order.created_at))
        
        total_count = query.count()
        offset = (page - 1) * page_size
        orders = query.offset(offset).limit(page_size).all()
        
        return orders, total_count
    
    @staticmethod
    def update_order(db: Session, order_id: int, order_data: OrderUpdateSchema) -> Optional[Order]:
        """Update order"""
        db_order = OrderService.get_order_by_id(db, order_id)
        if not db_order:
            return None
        
        update_data = order_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)
        
        db.commit()
        db.refresh(db_order)
        return db_order
    
    @staticmethod
    def get_all_orders(db: Session, page: int = 1, page_size: int = 10) -> Tuple[List[Order], int]:
        """Get all orders (admin only)"""
        query = db.query(Order).order_by(desc(Order.created_at))
        
        total_count = query.count()
        offset = (page - 1) * page_size
        orders = query.offset(offset).limit(page_size).all()
        
        return orders, total_count