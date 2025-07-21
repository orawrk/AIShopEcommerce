"""
Database configuration and connection management
Simplified to use direct MySQL connection without SQLAlchemy
"""

import pymysql
import logging

logger = logging.getLogger(__name__)

# MySQL Database configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'ecommerce',
    'unix_socket': '/tmp/mysql.sock',
    'charset': 'utf8mb4'
}

def get_connection():
    """Get database connection"""
    return pymysql.connect(**DATABASE_CONFIG)

async def create_tables():
    """Create database tables"""
    try:
        # Import and use the same database initialization from main app
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        from database import init_database
        init_database()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        # Don't raise to allow app to continue
        pass

def get_database():
    """Database dependency for FastAPI - returns MySQL connection"""
    conn = get_connection()
    try:
        yield conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

async def test_connection():
    """Test database connection"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False