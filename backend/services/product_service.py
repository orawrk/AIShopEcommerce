"""
Product Service Layer - Business Logic for Product Operations

This service layer implements the core business logic for product management in the
AI-powered e-commerce platform. It handles all product-related operations including
CRUD operations, inventory management, search functionality, and data validation.

Key Responsibilities:
- Product creation, retrieval, updating, and deletion
- Advanced search and filtering with pagination
- Inventory management and stock tracking
- Data validation and business rule enforcement
- Integration with authentic product catalog

Design Patterns:
- Service Layer Pattern: Separates business logic from controllers
- Repository Pattern: Abstracts data access operations
- Static Methods: Stateless operations for better performance

Author: AI E-Commerce Platform Team
Version: 1.0.0
"""

from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models.product import Product
from models.enums import ProductCategoryEnum, ProductSortByEnum, SortOrderEnum
from schemas.product_schemas import ProductCreateSchema, ProductUpdateSchema, ProductSearchSchema
import uuid


class ProductService:
    """
    Product service layer implementing comprehensive business logic for product operations.
    
    This class provides static methods for all product-related business operations,
    ensuring data integrity, validation, and proper error handling. It serves as
    the interface between the API controllers and the database models.
    
    Features:
    - CRUD operations with validation
    - Advanced search and filtering
    - Pagination support
    - Inventory management
    - Business rule enforcement
    """
    
    @staticmethod
    def create_product(db: Session, product_data: ProductCreateSchema) -> Product:
        """Create a new product"""
        # Generate unique SKU if not provided
        if not hasattr(product_data, 'sku') or not product_data.sku:
            product_data.sku = f"SKU-{uuid.uuid4().hex[:8].upper()}"
        
        db_product = Product(**product_data.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    
    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return db.query(Product).filter(
            and_(Product.id == product_id, Product.is_active == 1)
        ).first()
    
    @staticmethod
    def get_product_by_sku(db: Session, sku: str) -> Optional[Product]:
        """Get product by SKU"""
        return db.query(Product).filter(
            and_(Product.sku == sku, Product.is_active == 1)
        ).first()
    
    @staticmethod
    def get_products(db: Session, search_params: ProductSearchSchema) -> tuple[List[Product], int]:
        """Get products with search, filter, and pagination"""
        query = db.query(Product).filter(Product.is_active == 1)
        
        # Apply search filters
        if search_params.search_term:
            search_filter = or_(
                Product.name.ilike(f"%{search_params.search_term}%"),
                Product.description.ilike(f"%{search_params.search_term}%")
            )
            query = query.filter(search_filter)
        
        if search_params.category:
            query = query.filter(Product.category == search_params.category)
        
        if search_params.min_price is not None:
            query = query.filter(Product.price >= search_params.min_price)
        
        if search_params.max_price is not None:
            query = query.filter(Product.price <= search_params.max_price)
        
        # Apply sorting
        sort_column = getattr(Product, search_params.sort_by.value)
        if search_params.sort_order == SortOrderEnum.DESC:
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # Get total count before pagination
        total_count = query.count()
        
        # Apply pagination
        offset = (search_params.page - 1) * search_params.page_size
        products = query.offset(offset).limit(search_params.page_size).all()
        
        return products, total_count
    
    @staticmethod
    def update_product(db: Session, product_id: int, product_data: ProductUpdateSchema) -> Optional[Product]:
        """Update product"""
        db_product = ProductService.get_product_by_id(db, product_id)
        if not db_product:
            return None
        
        update_data = product_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        
        db.commit()
        db.refresh(db_product)
        return db_product
    
    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        """Soft delete product"""
        db_product = ProductService.get_product_by_id(db, product_id)
        if not db_product:
            return False
        
        db_product.is_active = 0
        db.commit()
        return True
    
    @staticmethod
    def update_stock(db: Session, product_id: int, quantity_change: int) -> Optional[Product]:
        """Update product stock quantity"""
        db_product = ProductService.get_product_by_id(db, product_id)
        if not db_product:
            return None
        
        new_quantity = db_product.stock_quantity + quantity_change
        if new_quantity < 0:
            raise ValueError("Insufficient stock")
        
        db_product.stock_quantity = new_quantity
        db.commit()
        db.refresh(db_product)
        return db_product