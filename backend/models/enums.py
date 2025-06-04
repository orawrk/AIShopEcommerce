"""
Application enums and constants
"""

from enum import Enum


class OrderStatusEnum(str, Enum):
    """Order status enumeration"""
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class ProductCategoryEnum(str, Enum):
    """Product category enumeration"""
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"
    HOME_GARDEN = "home_garden"
    SPORTS = "sports"


class UserRoleEnum(str, Enum):
    """User role enumeration"""
    CUSTOMER = "customer"
    ADMIN = "admin"
    MANAGER = "manager"


class SortOrderEnum(str, Enum):
    """Sort order enumeration"""
    ASC = "asc"
    DESC = "desc"


class ProductSortByEnum(str, Enum):
    """Product sorting fields enumeration"""
    NAME = "name"
    PRICE = "price"
    RATING = "rating"
    CREATED_AT = "created_at"