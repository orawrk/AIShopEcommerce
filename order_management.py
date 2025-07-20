"""
Enhanced order management with TEMP/CLOSE status system
"""
from database import get_connection
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

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
        cursor.execute("SELECT price, stock FROM products WHERE id = %s", (product_id,))
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
            SELECT oi.product_id, p.name, oi.quantity, oi.price, p.stock
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
            
            cursor.execute("UPDATE products SET stock = stock - %s WHERE id = %s", (quantity, product_id))
        
        # Update order status and shipping address
        cursor.execute("""
            UPDATE orders SET status = 'CLOSE', shipping_address = %s 
            WHERE id = %s
        """, (shipping_address, order_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
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