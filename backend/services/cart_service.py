"""
Cart service layer for business logic
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.cart import CartItem
from ..models.product import Product
from ..schemas.cart_schemas import CartItemCreateSchema, CartItemUpdateSchema


class CartService:
    """Cart service for business logic operations"""
    
    @staticmethod
    def add_to_cart(db: Session, user_id: int, item_data: CartItemCreateSchema) -> CartItem:
        """Add item to cart or update quantity if exists"""
        # Check if product exists
        product = db.query(Product).filter(Product.id == item_data.product_id).first()
        if not product:
            raise ValueError("Product not found")
        
        # Check if item already exists in cart
        existing_item = db.query(CartItem).filter(
            and_(
                CartItem.user_id == user_id,
                CartItem.product_id == item_data.product_id
            )
        ).first()
        
        if existing_item:
            # Update quantity
            existing_item.quantity += item_data.quantity
            db.commit()
            db.refresh(existing_item)
            return existing_item
        else:
            # Create new cart item
            cart_item = CartItem(
                user_id=user_id,
                product_id=item_data.product_id,
                quantity=item_data.quantity
            )
            db.add(cart_item)
            db.commit()
            db.refresh(cart_item)
            return cart_item
    
    @staticmethod
    def get_cart_items(db: Session, user_id: int) -> List[CartItem]:
        """Get all cart items for user"""
        return db.query(CartItem).filter(CartItem.user_id == user_id).all()
    
    @staticmethod
    def update_cart_item(db: Session, user_id: int, item_id: int, item_data: CartItemUpdateSchema) -> Optional[CartItem]:
        """Update cart item quantity"""
        cart_item = db.query(CartItem).filter(
            and_(
                CartItem.id == item_id,
                CartItem.user_id == user_id
            )
        ).first()
        
        if not cart_item:
            return None
        
        if item_data.quantity <= 0:
            # Remove item if quantity is 0 or negative
            db.delete(cart_item)
            db.commit()
            return None
        
        cart_item.quantity = item_data.quantity
        db.commit()
        db.refresh(cart_item)
        return cart_item
    
    @staticmethod
    def remove_from_cart(db: Session, user_id: int, item_id: int) -> bool:
        """Remove item from cart"""
        cart_item = db.query(CartItem).filter(
            and_(
                CartItem.id == item_id,
                CartItem.user_id == user_id
            )
        ).first()
        
        if not cart_item:
            return False
        
        db.delete(cart_item)
        db.commit()
        return True
    
    @staticmethod
    def clear_cart(db: Session, user_id: int) -> None:
        """Clear all items from user's cart"""
        db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        db.commit()
    
    @staticmethod
    def get_cart_total(db: Session, user_id: int) -> float:
        """Calculate total amount for cart"""
        cart_items = CartService.get_cart_items(db, user_id)
        total = 0.0
        
        for item in cart_items:
            if item.product:
                total += item.product.price * item.quantity
        
        return total