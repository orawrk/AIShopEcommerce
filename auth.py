"""
Authentication module for user login/logout functionality
"""
import hashlib
import streamlit as st
import json
import os
from database import get_connection
import logging

logger = logging.getLogger(__name__)

USER_DATA_FILE = "user_data.json"

def load_user_data():
    """Load user data from JSON file"""
    try:
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'r') as f:
                return json.load(f)
        else:
            return {"users": {}}
    except Exception as e:
        logger.error(f"Error loading user data: {e}")
        return {"users": {}}

def save_user_data(data):
    """Save user data to JSON file"""
    try:
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info("User data saved to file")
    except Exception as e:
        logger.error(f"Error saving user data: {e}")

def sync_user_to_file(username, email, password_hash, first_name, last_name, phone, country, city):
    """Save user data to file for persistence"""
    try:
        data = load_user_data()
        data["users"][username] = {
            "email": email,
            "password_hash": password_hash,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "country": country,
            "city": city
        }
        save_user_data(data)
        return True
    except Exception as e:
        logger.error(f"Error syncing user to file: {e}")
        return False

def load_users_from_file_to_db():
    """Load users from file to database on startup"""
    try:
        data = load_user_data()
        if not data["users"]:
            return
            
        conn = get_connection()
        cursor = conn.cursor()
        
        for username, user_info in data["users"].items():
            # Check if user already exists in database
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if not cursor.fetchone():
                # Insert user into database
                cursor.execute("""
                    INSERT INTO users (username, email, password_hash, first_name, last_name, phone, country, city) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    username,
                    user_info["email"],
                    user_info["password_hash"],
                    user_info["first_name"],
                    user_info["last_name"],
                    user_info["phone"],
                    user_info["country"],
                    user_info["city"]
                ))
        
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("Users loaded from file to database")
        
    except Exception as e:
        logger.error(f"Error loading users from file: {e}")

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """Verify password against hash"""
    return hash_password(password) == hashed_password

def create_user(username, email, password, first_name, last_name, phone, country, city):
    """Create a new user account - with file fallback"""
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
        
        # Also save to file for persistence
        sync_user_to_file(username, email, hashed_pwd, first_name, last_name, phone, country, city)
        
        return True, "Account created successfully"
        
    except Exception as e:
        logger.error(f"Database create failed, trying file only: {e}")
        # Fallback to file-only registration
        try:
            # Check if user already exists in file
            data = load_user_data()
            if username in data["users"]:
                return False, "Username already exists"
            
            # Check email in file
            for existing_user in data["users"].values():
                if existing_user["email"] == email:
                    return False, "Email already exists"
            
            # Create user in file
            hashed_pwd = hash_password(password)
            if sync_user_to_file(username, email, hashed_pwd, first_name, last_name, phone, country, city):
                return True, "Account created successfully (saved to file)"
            else:
                return False, "Failed to create account"
                
        except Exception as file_error:
            logger.error(f"File create also failed: {file_error}")
            return False, f"Error creating account: {str(file_error)}"

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
        logger.error(f"Database authentication failed, trying file: {e}")
        # Fallback to file-based authentication
        try:
            data = load_user_data()
            if username in data["users"]:
                user_info = data["users"][username]
                if verify_password(password, user_info["password_hash"]):
                    return {
                        'id': 1,  # Default ID for file-based users
                        'username': username,
                        'email': user_info["email"],
                        'first_name': user_info["first_name"],
                        'last_name': user_info["last_name"]
                    }
            return None
        except Exception as file_error:
            logger.error(f"File authentication also failed: {file_error}")
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