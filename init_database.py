#!/usr/bin/env python3
"""
Database initialization script for AI Shopping Platform
Creates database, tables, and loads sample data
"""

import pymysql
import sys

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'unix_socket': '/tmp/mysql.sock',
    'charset': 'utf8mb4'
}

def get_connection(database=None):
    """Get database connection"""
    config = DATABASE_CONFIG.copy()
    if database:
        config['database'] = database
    return pymysql.connect(**config)

def create_database():
    """Create the ecommerce database"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ecommerce")
        cursor.execute("USE ecommerce")
        print("✅ Database 'ecommerce' created successfully")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_tables():
    """Create all required tables"""
    try:
        conn = get_connection('ecommerce')
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                phone VARCHAR(50),
                country VARCHAR(100),
                city VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10,2) NOT NULL,
                category VARCHAR(100) NOT NULL,
                stock_quantity INT NOT NULL DEFAULT 0,
                rating DECIMAL(3,2) DEFAULT 4.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                status ENUM('TEMP', 'CLOSE') DEFAULT 'TEMP',
                shipping_address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Order items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL DEFAULT 1,
                price DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        """)
        
        # Favorites table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                product_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_favorite (user_id, product_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ All tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def insert_sample_products():
    """Insert sample product data"""
    try:
        conn = get_connection('ecommerce')
        cursor = conn.cursor()
        
        # Check if products already exist
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"✅ Products already exist ({count} products)")
            cursor.close()
            conn.close()
            return True
        
        # Sample products data
        products = [
            ("Gaming Laptop", "High-performance gaming laptop with RTX graphics", 1299.99, "Electronics", 15, 4.5),
            ("Wireless Headphones", "Premium noise-canceling wireless headphones", 199.99, "Electronics", 32, 4.3),
            ("Smart Watch", "Fitness tracking smartwatch with heart rate monitor", 249.99, "Electronics", 28, 4.2),
            ("Office Chair", "Ergonomic office chair with lumbar support", 159.99, "Furniture", 12, 4.1),
            ("Coffee Table", "Modern glass coffee table for living room", 89.99, "Furniture", 8, 4.0),
            ("Bookshelf", "5-tier wooden bookshelf for home or office", 79.99, "Furniture", 15, 4.2),
            ("Running Shoes", "Lightweight running shoes for daily training", 89.99, "Sports", 45, 4.4),
            ("Yoga Mat", "Non-slip yoga mat for exercise and meditation", 29.99, "Sports", 67, 4.3),
            ("Basketball", "Official size basketball for outdoor play", 24.99, "Sports", 23, 4.1),
            ("Winter Coat", "Warm winter coat with waterproof exterior", 129.99, "Clothing", 18, 4.2),
            ("Casual T-Shirt", "Comfortable cotton t-shirt in various colors", 19.99, "Clothing", 89, 4.0),
            ("Jeans", "Classic blue jeans with modern fit", 59.99, "Clothing", 34, 4.1),
            ("Smartphone", "Latest 5G smartphone with advanced camera", 799.99, "Electronics", 22, 4.6),
            ("Tablet", "10-inch tablet for work and entertainment", 329.99, "Electronics", 19, 4.3),
            ("Sunglasses", "UV protection sunglasses with polarized lenses", 79.99, "Accessories", 41, 4.2),
            ("Backpack", "Durable backpack for travel and daily use", 49.99, "Accessories", 38, 4.1),
            ("Water Bottle", "Insulated stainless steel water bottle", 24.99, "Accessories", 76, 4.0),
            ("Desk Lamp", "LED desk lamp with adjustable brightness", 39.99, "Home", 25, 4.2),
            ("Wall Clock", "Modern wall clock for home decoration", 34.99, "Home", 31, 4.0),
            ("Plant Pot", "Ceramic plant pot with drainage tray", 14.99, "Home", 55, 3.9)
        ]
        
        # Insert products
        insert_query = """
            INSERT INTO products (name, description, price, category, stock_quantity, rating)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(insert_query, products)
        conn.commit()
        
        print(f"✅ Inserted {len(products)} sample products")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error inserting sample products: {e}")
        return False

def main():
    """Main initialization function"""
    print("🚀 Initializing AI Shopping Platform Database...")
    
    # Create database
    if not create_database():
        sys.exit(1)
    
    # Create tables
    if not create_tables():
        sys.exit(1)
    
    # Insert sample data
    if not insert_sample_products():
        sys.exit(1)
    
    print("🎉 Database initialization completed successfully!")
    print("📊 Database: ecommerce")
    print("📋 Tables: users, products, orders, order_items, favorites")
    print("🛍️ Sample Products: 20 items across 5 categories")

if __name__ == "__main__":
    main()