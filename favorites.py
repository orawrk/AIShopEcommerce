"""
Favorites management module
"""
from database import get_connection
import logging

logger = logging.getLogger(__name__)

def add_to_favorites(user_id, product_id):
    """Add product to user's favorites"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if already in favorites
        cursor.execute("SELECT id FROM favorites WHERE user_id = %s AND product_id = %s", (user_id, product_id))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "Product already in favorites"
        
        # Add to favorites
        cursor.execute("INSERT INTO favorites (user_id, product_id) VALUES (%s, %s)", (user_id, product_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, "Added to favorites"
        
    except Exception as e:
        logger.error(f"Error adding to favorites: {e}")
        return False, "Error adding to favorites"

def remove_from_favorites(user_id, product_id):
    """Remove product from user's favorites"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM favorites WHERE user_id = %s AND product_id = %s", (user_id, product_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, "Removed from favorites"
        
    except Exception as e:
        logger.error(f"Error removing from favorites: {e}")
        return False, "Error removing from favorites"

def get_user_favorites(user_id):
    """Get user's favorite products"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.id, p.name, p.description, p.price, p.category, p.stock, p.rating
            FROM products p
            JOIN favorites f ON p.id = f.product_id
            WHERE f.user_id = %s
            ORDER BY f.added_at DESC
        """, (user_id,))
        
        favorites = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return favorites
        
    except Exception as e:
        logger.error(f"Error getting favorites: {e}")
        return []

def is_favorite(user_id, product_id):
    """Check if product is in user's favorites"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM favorites WHERE user_id = %s AND product_id = %s", (user_id, product_id))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return result is not None
        
    except Exception as e:
        logger.error(f"Error checking favorite: {e}")
        return False