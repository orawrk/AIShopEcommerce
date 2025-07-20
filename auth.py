"""
Authentication module for user login/logout functionality
"""
import hashlib
import streamlit as st
from database import get_connection
import logging

logger = logging.getLogger(__name__)

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """Verify password against hash"""
    return hash_password(password) == hashed_password

def create_user(username, email, password, first_name, last_name, phone, country, city):
    """Create a new user account"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return False, "Username already exists"
        
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return False, "Email already exists"
        
        # Create new user
        hashed_pwd = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, first_name, last_name, phone, country, city) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (username, email, hashed_pwd, first_name, last_name, phone, country, city))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, "Account created successfully"
        
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return False, f"Error creating account: {str(e)}"

def authenticate_user(username, password):
    """Authenticate user login"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, password_hash, first_name, last_name 
            FROM users WHERE username = %s
        """, (username,))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and verify_password(password, user[3]):
            return {
                'id': user[0],
                'username': user[1], 
                'email': user[2],
                'first_name': user[4],
                'last_name': user[5]
            }
        
        return None
        
    except Exception as e:
        logger.error(f"Error authenticating user: {e}")
        return None

def get_user_by_id(user_id):
    """Get user information by ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, first_name, last_name, phone, country, city
            FROM users WHERE id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2], 
                'first_name': user[3],
                'last_name': user[4],
                'phone': user[5],
                'country': user[6],
                'city': user[7]
            }
        
        return None
        
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        return None

def delete_user_account(user_id):
    """Delete user account and all associated data"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Delete user's orders and associated data
        cursor.execute("DELETE FROM order_items WHERE order_id IN (SELECT id FROM orders WHERE user_id = %s)", (user_id,))
        cursor.execute("DELETE FROM orders WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM favorites WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM user_behavior WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, "Account deleted successfully"
        
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        return False, f"Error deleting account: {str(e)}"