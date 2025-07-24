"""
Enhanced order management with TEMP/CLOSE status system
"""
from database import get_connection
import logging
from datetime import datetime
import json
import os

logger = logging.getLogger(__name__)

ORDER_HISTORY_FILE = "order_history.json"

def create_temp_order(user_id, shipping_address=""):
    """Create a new temporary order"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if user already has a temp order
        cursor.execute("SELECT id FROM orders WHERE user_id = %s AND status = 'TEMP'", (user_id,))
        existing = cursor.fetchone()
        
        if existing:
            cursor.close()
            conn.close()
            return existing[0]  # Return existing temp order ID
        
        # Create new temp order
        cursor.execute("""
            INSERT INTO orders (user_id, total_amount, status, shipping_address, created_at) 
            VALUES (%s, 0.00, 'TEMP', %s, %s)
        """, (user_id, shipping_address, datetime.now()))
        
        order_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        
        return order_id
        
    except Exception as e:
        logger.error(f"Error creating temp order: {e}")
        return None

def add_item_to_temp_order(user_id, product_id, quantity=1):
    """Add item to user's temp order"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get or create temp order
        order_id = create_temp_order(user_id)
        if not order_id:
            return False, "Could not create order"
        
        # Get product price and check stock
        cursor.execute("SELECT price, stock_quantity FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            cursor.close()
            conn.close()
            return False, "Product not found"
        
        price, stock = product
        if stock < quantity:
            cursor.close()
            conn.close()
            return False, "Not enough items in stock"
        
        # Check if item already in order
        cursor.execute("SELECT id, quantity FROM order_items WHERE order_id = %s AND product_id = %s", (order_id, product_id))
        existing = cursor.fetchone()
        
        if existing:
            # Update quantity
            new_quantity = existing[1] + quantity
            if stock < new_quantity:
                cursor.close()
                conn.close()
                return False, "Not enough items in stock"
            
            cursor.execute("UPDATE order_items SET quantity = %s WHERE id = %s", (new_quantity, existing[0]))
        else:
            # Add new item
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, price) 
                VALUES (%s, %s, %s, %s)
            """, (order_id, product_id, quantity, price))
        
        # Update order total
        cursor.execute("""
            UPDATE orders SET total_amount = (
                SELECT SUM(quantity * price) FROM order_items WHERE order_id = %s
            ) WHERE id = %s
        """, (order_id, order_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, "Item added to order"
        
    except Exception as e:
        logger.error(f"Error adding item to order: {e}")
        return False, "Error adding item to order"

def remove_item_from_temp_order(user_id, product_id):
    """Remove item from user's temp order"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get temp order
        cursor.execute("SELECT id FROM orders WHERE user_id = %s AND status = 'TEMP'", (user_id,))
        order = cursor.fetchone()
        if not order:
            cursor.close()
            conn.close()
            return False, "No temp order found"
        
        order_id = order[0]
        
        # Remove item
        cursor.execute("DELETE FROM order_items WHERE order_id = %s AND product_id = %s", (order_id, product_id))
        
        # Update order total
        cursor.execute("""
            UPDATE orders SET total_amount = (
                SELECT COALESCE(SUM(quantity * price), 0) FROM order_items WHERE order_id = %s
            ) WHERE id = %s
        """, (order_id, order_id))
        
        # Check if order is empty, delete if so
        cursor.execute("SELECT COUNT(*) FROM order_items WHERE order_id = %s", (order_id,))
        item_count = cursor.fetchone()[0]
        
        if item_count == 0:
            cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, "Item removed from order"
        
    except Exception as e:
        logger.error(f"Error removing item from order: {e}")
        return False, "Error removing item from order"

def get_temp_order(user_id):
    """Get user's temp order with items"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get temp order
        cursor.execute("""
            SELECT id, total_amount, shipping_address, created_at 
            FROM orders WHERE user_id = %s AND status = 'TEMP'
        """, (user_id,))
        
        order = cursor.fetchone()
        if not order:
            cursor.close()
            conn.close()
            return None
        
        order_id, total_amount, shipping_address, created_at = order
        
        # Get order items
        cursor.execute("""
            SELECT oi.product_id, p.name, oi.quantity, oi.price, p.stock_quantity
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
        """, (order_id,))
        
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {
            'id': order_id,
            'total_amount': total_amount,
            'shipping_address': shipping_address,
            'created_at': created_at,
            'items': items
        }
        
    except Exception as e:
        logger.error(f"Error getting temp order: {e}")
        return None

def complete_order(user_id, shipping_address):
    """Complete temp order and change status to CLOSE"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get temp order
        order = get_temp_order(user_id)
        if not order:
            cursor.close()
            conn.close()
            return False, "No temp order found"
        
        order_id = order['id']
        
        # Update stock for all items
        for item in order['items']:
            product_id, name, quantity, price, stock = item
            if stock < quantity:
                cursor.close()
                conn.close()
                return False, f"Not enough {name} in stock"
            
            cursor.execute("UPDATE products SET stock_quantity = stock_quantity - %s WHERE id = %s", (quantity, product_id))
        
        # Update order status and shipping address
        cursor.execute("""
            UPDATE orders SET status = 'CLOSE', shipping_address = %s 
            WHERE id = %s
        """, (shipping_address, order_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Save completed order to persistent file
        save_completed_order(user_id, order_id, shipping_address, order['total_amount'], order['items'])
        
        return True, "Order completed successfully"
        
    except Exception as e:
        logger.error(f"Error completing order: {e}")
        return False, "Error completing order"

def get_user_orders(user_id, status=None):
    """Get user's orders (all or filtered by status)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute("""
                SELECT id, total_amount, status, shipping_address, created_at 
                FROM orders WHERE user_id = %s AND status = %s 
                ORDER BY created_at DESC
            """, (user_id, status))
        else:
            cursor.execute("""
                SELECT id, total_amount, status, shipping_address, created_at 
                FROM orders WHERE user_id = %s 
                ORDER BY CASE WHEN status = 'TEMP' THEN 0 ELSE 1 END, created_at DESC
            """, (user_id,))
        
        orders = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return orders
        
    except Exception as e:
        logger.error(f"Error getting orders: {e}")
        return []

def get_order_items(order_id):
    """Get items for a specific order"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT oi.product_id, p.name, oi.quantity, oi.price, 
                   (oi.quantity * oi.price) as subtotal
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
        """, (order_id,))
        
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return items
        
    except Exception as e:
        logger.error(f"Error getting order items: {e}")
        return []

def load_order_history():
    """Load order history from file"""
    try:
        if os.path.exists(ORDER_HISTORY_FILE):
            with open(ORDER_HISTORY_FILE, 'r') as f:
                return json.load(f)
        return {"orders": {}}
    except Exception as e:
        logger.error(f"Error loading order history: {e}")
        return {"orders": {}}

def save_order_history(data):
    """Save order history to file"""
    try:
        with open(ORDER_HISTORY_FILE, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        logger.info("Order history saved to file")
    except Exception as e:
        logger.error(f"Error saving order history: {e}")

def save_completed_order(user_id, order_id, shipping_address, total_amount, items):
    """Save completed order to persistent storage"""
    try:
        data = load_order_history()
        
        if str(user_id) not in data["orders"]:
            data["orders"][str(user_id)] = []
        
        # Create order record
        order_record = {
            "order_id": order_id,
            "total_amount": float(total_amount),
            "shipping_address": shipping_address,
            "completed_at": datetime.now().isoformat(),
            "status": "CLOSE",
            "items": []
        }
        
        # Add items
        for item in items:
            product_id, name, quantity, price, stock = item
            order_record["items"].append({
                "product_id": product_id,
                "name": name,
                "quantity": quantity,
                "price": float(price),
                "subtotal": float(quantity * price)
            })
        
        data["orders"][str(user_id)].append(order_record)
        save_order_history(data)
        
        logger.info(f"Saved completed order {order_id} for user {user_id}")
        
    except Exception as e:
        logger.error(f"Error saving completed order: {e}")

def load_user_orders_from_file(user_id):
    """Load user's order history from file"""
    try:
        data = load_order_history()
        user_orders = data["orders"].get(str(user_id), [])
        
        # Sync with database if needed
        sync_orders_to_database(user_id, user_orders)
        
        return user_orders
        
    except Exception as e:
        logger.error(f"Error loading user orders from file: {e}")
        return []

def sync_orders_to_database(user_id, file_orders):
    """Sync order history from file to database"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        for order in file_orders:
            # Check if order exists in database
            cursor.execute("SELECT id FROM orders WHERE id = %s", (order["order_id"],))
            if not cursor.fetchone():
                # Create order in database
                cursor.execute("""
                    INSERT INTO orders (id, user_id, total_amount, status, shipping_address, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                    total_amount = VALUES(total_amount),
                    status = VALUES(status),
                    shipping_address = VALUES(shipping_address)
                """, (
                    order["order_id"],
                    user_id,
                    order["total_amount"],
                    order["status"],
                    order["shipping_address"],
                    order["completed_at"]
                ))
                
                # Add order items
                for item in order["items"]:
                    cursor.execute("""
                        INSERT IGNORE INTO order_items (order_id, product_id, quantity, price)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        order["order_id"],
                        item["product_id"],
                        item["quantity"],
                        item["price"]
                    ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"Synced {len(file_orders)} orders to database for user {user_id}")
        
    except Exception as e:
        logger.error(f"Error syncing orders to database: {e}")

def get_combined_user_orders(user_id):
    """Get user orders from both database and file, ensuring consistency"""
    try:
        # Load from file first
        file_orders = load_user_orders_from_file(user_id)
        
        # Get from database
        db_orders = get_user_orders(user_id)
        
        # Combine and deduplicate
        combined_orders = []
        
        # Add database orders
        for order in db_orders:
            order_id, total_amount, status, shipping_address, created_at = order
            combined_orders.append({
                "order_id": order_id,
                "total_amount": float(total_amount),
                "status": status,
                "shipping_address": shipping_address,
                "created_at": str(created_at),
                "source": "database"
            })
        
        # Add file orders not in database
        db_order_ids = [order[0] for order in db_orders]
        for file_order in file_orders:
            if file_order["order_id"] not in db_order_ids:
                file_order["source"] = "file"
                combined_orders.append(file_order)
        
        # Sort by creation date (most recent first)
        combined_orders.sort(key=lambda x: x.get("completed_at", x.get("created_at", "")), reverse=True)
        
        return combined_orders
        
    except Exception as e:
        logger.error(f"Error getting combined user orders: {e}")
        return []