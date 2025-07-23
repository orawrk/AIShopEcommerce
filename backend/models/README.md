# Backend Models Directory

**Note**: This directory contains deprecated SQLAlchemy model files from a previous implementation.

## Current Implementation

The AI Shopping Platform now uses **direct PyMySQL connections** with raw SQL queries instead of SQLAlchemy ORM. This provides:

- **Simplified Architecture**: No ORM complexity
- **Better Performance**: Direct database access without ORM overhead  
- **Full SQL Control**: Write optimized queries for specific needs
- **Easier Maintenance**: Straightforward database operations

## Database Operations

All current database operations are handled in:
- `database.py` - Core database functions using PyMySQL
- `auth.py` - User authentication operations
- `order_management.py` - Order and cart management  
- `favorites.py` - User favorites functionality

## Legacy Files in this Directory

The following files are kept for reference but are **NOT USED** in the current implementation:
- `base.py` - SQLAlchemy base model
- `user.py` - User SQLAlchemy model
- `product.py` - Product SQLAlchemy model  
- `order.py` - Order SQLAlchemy model
- `cart.py` - Cart SQLAlchemy model
- `user_behavior.py` - User behavior SQLAlchemy model
- `enums.py` - Database enums

## Current Database Schema

The database schema is defined and managed through direct SQL statements in the main application files, providing better control and transparency over the database structure.

**Created by: Ora Weinstein | 2025**