import sqlite3
import pandas as pd
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)

DATABASE_PATH = "ecommerce.db"

def get_connection():
    """Get database connection"""
    return sqlite3.connect(DATABASE_PATH)

def init_database():
    """Initialize database with tables and sample data"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                category TEXT,
                stock INTEGER DEFAULT 0,
                rating REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER DEFAULT 1,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                total_amount REAL,
                status TEXT DEFAULT 'Processing',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                price REAL,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_behavior (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT,
                product_id INTEGER,
                session_duration REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        conn.commit()
        
        # Check if we need to populate sample data
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        
        if product_count == 0:
            populate_sample_data(conn)
        
        conn.close()
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise

def populate_sample_data(conn):
    """Populate database with sample products and users"""
    cursor = conn.cursor()
    
    # Sample products
    products = [
        ("MacBook Pro 16-inch", "High-performance laptop with M2 chip", 2499.99, "Electronics", 15, 4.8),
        ("iPhone 15 Pro", "Latest smartphone with advanced camera system", 999.99, "Electronics", 25, 4.7),
        ("Samsung 4K Smart TV", "55-inch QLED display with smart features", 799.99, "Electronics", 10, 4.5),
        ("Nike Air Max", "Comfortable running shoes for daily training", 129.99, "Sports", 50, 4.3),
        ("Levi's Jeans", "Classic blue denim jeans", 79.99, "Clothing", 30, 4.2),
        ("Python Programming Book", "Complete guide to Python programming", 49.99, "Books", 20, 4.6),
        ("Coffee Maker", "Automatic drip coffee maker with timer", 89.99, "Home & Garden", 18, 4.1),
        ("Wireless Headphones", "Noise-cancelling over-ear headphones", 199.99, "Electronics", 35, 4.4),
        ("Yoga Mat", "Non-slip exercise mat for yoga and fitness", 29.99, "Sports", 40, 4.0),
        ("Kitchen Knife Set", "Professional chef knives with wooden block", 149.99, "Home & Garden", 12, 4.7)
    ]
    
    cursor.executemany(
        "INSERT INTO products (name, description, price, category, stock, rating) VALUES (?, ?, ?, ?, ?, ?)",
        products
    )
    
    # Sample user
    cursor.execute("INSERT OR IGNORE INTO users (id, username, email) VALUES (1, 'demo_user', 'demo@example.com')")
    
    conn.commit()
    logger.info("Sample data populated successfully")

def get_products(search_term=None, category=None, sort_by=None):
    """Get products with optional filtering and sorting"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT id, name, description, price, category, stock, rating FROM products WHERE 1=1"
        params = []
        
        if search_term:
            query += " AND (name LIKE ? OR description LIKE ?)"
            params.extend([f"%{search_term}%", f"%{search_term}%"])
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        # Add sorting
        if sort_by == "Price (Low to High)":
            query += " ORDER BY price ASC"
        elif sort_by == "Price (High to Low)":
            query += " ORDER BY price DESC"
        elif sort_by == "Rating":
            query += " ORDER BY rating DESC"
        else:
            query += " ORDER BY name ASC"
        
        cursor.execute(query, params)
        products = cursor.fetchall()
        conn.close()
        
        return products
        
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        return []

def add_to_cart(user_id, product_id, quantity):
    """Add item to cart"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if item already exists in cart
        cursor.execute(
            "SELECT id, quantity FROM cart WHERE user_id = ? AND product_id = ?",
            (user_id, product_id)
        )
        existing_item = cursor.fetchone()
        
        if existing_item:
            # Update quantity
            new_quantity = existing_item[1] + quantity
            cursor.execute(
                "UPDATE cart SET quantity = ? WHERE id = ?",
                (new_quantity, existing_item[0])
            )
        else:
            # Add new item
            cursor.execute(
                "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
                (user_id, product_id, quantity)
            )
        
        conn.commit()
        conn.close()
        
        # Log user behavior
        log_user_behavior(user_id, "add_to_cart", product_id)
        
        return True
        
    except Exception as e:
        logger.error(f"Error adding to cart: {e}")
        return False

def get_cart_items(user_id):
    """Get cart items for user"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.id, p.name, p.price, c.quantity, p.id
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = ?
        ''', (user_id,))
        
        items = cursor.fetchall()
        conn.close()
        
        return items
        
    except Exception as e:
        logger.error(f"Error fetching cart items: {e}")
        return []

def create_order(user_id, cart_items, total_amount):
    """Create order from cart items"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create order
        cursor.execute(
            "INSERT INTO orders (user_id, total_amount) VALUES (?, ?)",
            (user_id, total_amount)
        )
        order_id = cursor.lastrowid
        
        # Add order items
        for item in cart_items:
            cart_id, product_name, price, quantity, product_id = item
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
                (order_id, product_id, quantity, price)
            )
            
            # Update product stock
            cursor.execute(
                "UPDATE products SET stock = stock - ? WHERE id = ?",
                (quantity, product_id)
            )
        
        # Clear cart
        cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        
        conn.commit()
        conn.close()
        
        # Log user behavior
        log_user_behavior(user_id, "purchase", None)
        
        return order_id
        
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        return None

def get_user_orders(user_id):
    """Get orders for user"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, created_at, total_amount, status FROM orders WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        
        orders = cursor.fetchall()
        conn.close()
        
        return orders
        
    except Exception as e:
        logger.error(f"Error fetching orders: {e}")
        return []

def update_inventory(product_id, new_stock):
    """Update product inventory"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE products SET stock = ? WHERE id = ?",
            (new_stock, product_id)
        )
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        logger.error(f"Error updating inventory: {e}")
        return False

def log_user_behavior(user_id, action, product_id=None, session_duration=None):
    """Log user behavior for ML training"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO user_behavior (user_id, action, product_id, session_duration) VALUES (?, ?, ?, ?)",
            (user_id, action, product_id, session_duration)
        )
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        logger.error(f"Error logging user behavior: {e}")

def get_user_behavior_data():
    """Get user behavior data for ML training"""
    try:
        conn = get_connection()
        
        query = '''
            SELECT ub.user_id, ub.action, ub.product_id, ub.session_duration,
                   COUNT(CASE WHEN ub2.action = 'purchase' THEN 1 END) as purchase_count,
                   COUNT(CASE WHEN ub2.action = 'add_to_cart' THEN 1 END) as cart_count,
                   AVG(o.total_amount) as avg_order_value
            FROM user_behavior ub
            LEFT JOIN user_behavior ub2 ON ub.user_id = ub2.user_id
            LEFT JOIN orders o ON ub.user_id = o.user_id
            GROUP BY ub.user_id, ub.action, ub.product_id, ub.session_duration
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
        
    except Exception as e:
        logger.error(f"Error fetching behavior data: {e}")
        return pd.DataFrame()
