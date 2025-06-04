import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import os

logger = logging.getLogger(__name__)

def setup_logging():
    """Setup application logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )

def validate_email(email):
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_currency(amount):
    """Format currency for display"""
    return f"${amount:.2f}"

def calculate_discount(original_price, discount_percent):
    """Calculate discounted price"""
    discount_amount = original_price * (discount_percent / 100)
    return original_price - discount_amount

def generate_order_number():
    """Generate unique order number"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = np.random.randint(1000, 9999)
    return f"ORD-{timestamp}-{random_suffix}"

def calculate_shipping_cost(total_amount, shipping_threshold=50.0):
    """Calculate shipping cost based on order total"""
    if total_amount >= shipping_threshold:
        return 0.0  # Free shipping
    else:
        return 9.99  # Standard shipping fee

def get_estimated_delivery_date(processing_days=2, shipping_days=3):
    """Calculate estimated delivery date"""
    processing_time = timedelta(days=processing_days)
    shipping_time = timedelta(days=shipping_days)
    
    order_date = datetime.now()
    estimated_delivery = order_date + processing_time + shipping_time
    
    # Skip weekends for business days calculation
    while estimated_delivery.weekday() >= 5:  # 5=Saturday, 6=Sunday
        estimated_delivery += timedelta(days=1)
    
    return estimated_delivery.strftime("%B %d, %Y")

def sanitize_search_query(query):
    """Sanitize search query to prevent SQL injection"""
    if not query:
        return ""
    
    # Remove special characters that could be used for SQL injection
    import re
    sanitized = re.sub(r'[;\'\"\\]', '', query)
    return sanitized.strip()

def calculate_similarity(text1, text2):
    """Calculate text similarity for product recommendations"""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        return similarity
        
    except Exception as e:
        logger.error(f"Similarity calculation error: {e}")
        return 0.0

def generate_product_recommendations(user_purchase_history, all_products, num_recommendations=3):
    """Generate product recommendations based on purchase history"""
    try:
        if not user_purchase_history:
            # Return random popular products for new users
            return np.random.choice(all_products, 
                                  size=min(num_recommendations, len(all_products)), 
                                  replace=False).tolist()
        
        # Simple collaborative filtering approach
        recommendations = []
        purchased_categories = [p['category'] for p in user_purchase_history]
        
        # Find products in same categories
        for product in all_products:
            if (product['category'] in purchased_categories and 
                product not in user_purchase_history):
                recommendations.append(product)
        
        # Limit to requested number
        return recommendations[:num_recommendations]
        
    except Exception as e:
        logger.error(f"Recommendation generation error: {e}")
        return []

def export_data_to_csv(data, filename, directory="exports"):
    """Export data to CSV file"""
    try:
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        
        if isinstance(data, pd.DataFrame):
            data.to_csv(filepath, index=False)
        else:
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False)
        
        logger.info(f"Data exported to {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Export error: {e}")
        return None

def import_data_from_csv(filepath):
    """Import data from CSV file"""
    try:
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            logger.info(f"Data imported from {filepath}")
            return df
        else:
            logger.warning(f"File not found: {filepath}")
            return pd.DataFrame()
            
    except Exception as e:
        logger.error(f"Import error: {e}")
        return pd.DataFrame()

def backup_database(db_path="ecommerce.db", backup_dir="backups"):
    """Create database backup"""
    try:
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"ecommerce_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Copy database file
        import shutil
        shutil.copy2(db_path, backup_path)
        
        logger.info(f"Database backed up to {backup_path}")
        return backup_path
        
    except Exception as e:
        logger.error(f"Backup error: {e}")
        return None

def validate_product_data(product_data):
    """Validate product data before database insertion"""
    required_fields = ['name', 'price', 'category']
    
    for field in required_fields:
        if field not in product_data or not product_data[field]:
            return False, f"Missing required field: {field}"
    
    # Validate price
    try:
        price = float(product_data['price'])
        if price < 0:
            return False, "Price must be non-negative"
    except (ValueError, TypeError):
        return False, "Invalid price format"
    
    # Validate stock
    if 'stock' in product_data:
        try:
            stock = int(product_data['stock'])
            if stock < 0:
                return False, "Stock must be non-negative"
        except (ValueError, TypeError):
            return False, "Invalid stock format"
    
    return True, "Valid"

def calculate_metrics(data):
    """Calculate business metrics from data"""
    try:
        metrics = {}
        
        if 'orders' in data:
            orders = data['orders']
            metrics['total_orders'] = len(orders)
            metrics['total_revenue'] = sum([order.get('total_amount', 0) for order in orders])
            metrics['average_order_value'] = metrics['total_revenue'] / max(1, metrics['total_orders'])
        
        if 'users' in data:
            users = data['users']
            metrics['total_users'] = len(users)
            
            # Calculate active users (users with orders in last 30 days)
            thirty_days_ago = datetime.now() - timedelta(days=30)
            active_users = [u for u in users if u.get('last_order_date', '') > thirty_days_ago.isoformat()]
            metrics['active_users'] = len(active_users)
            metrics['user_activity_rate'] = metrics['active_users'] / max(1, metrics['total_users'])
        
        return metrics
        
    except Exception as e:
        logger.error(f"Metrics calculation error: {e}")
        return {}

def send_notification(user_id, message, notification_type="info"):
    """Send notification to user (placeholder for notification system)"""
    try:
        # In a real application, this would integrate with email, SMS, or push notification services
        logger.info(f"Notification to user {user_id}: {message} (type: {notification_type})")
        
        # Could integrate with services like:
        # - SendGrid for email
        # - Twilio for SMS  
        # - Firebase for push notifications
        
        notification_data = {
            'user_id': user_id,
            'message': message,
            'type': notification_type,
            'timestamp': datetime.now().isoformat(),
            'sent': True
        }
        
        return notification_data
        
    except Exception as e:
        logger.error(f"Notification error: {e}")
        return None
