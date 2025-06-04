import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, mean_squared_error
import pickle
import logging
import os
from database import get_user_behavior_data

logger = logging.getLogger(__name__)

class UserBehaviorPredictor:
    def __init__(self):
        self.churn_model = None
        self.spending_model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.is_trained = False
    
    def prepare_features(self, df):
        """Prepare features for ML models"""
        try:
            # Create user-level aggregations
            user_features = df.groupby('user_id').agg({
                'purchase_count': 'sum',
                'cart_count': 'sum',
                'avg_order_value': 'mean',
                'session_duration': 'mean'
            }).fillna(0)
            
            # Add derived features
            user_features['cart_to_purchase_ratio'] = (
                user_features['cart_count'] / (user_features['purchase_count'] + 1)
            )
            user_features['total_value'] = (
                user_features['purchase_count'] * user_features['avg_order_value']
            )
            
            # Create synthetic target variables for demonstration
            # In production, these would come from actual business metrics
            user_features['days_since_last_purchase'] = np.random.randint(1, 365, len(user_features))
            user_features['churn'] = (user_features['days_since_last_purchase'] > 90).astype(int)
            user_features['next_month_spending'] = np.maximum(0, 
                user_features['avg_order_value'] + np.random.normal(0, 50, len(user_features))
            )
            
            return user_features
            
        except Exception as e:
            logger.error(f"Feature preparation error: {e}")
            return pd.DataFrame()
    
    def train_models(self):
        """Train churn prediction and spending prediction models"""
        try:
            logger.info("Starting model training...")
            
            # Load training data
            training_data = self.load_training_data()
            
            if training_data.empty:
                logger.warning("No training data available, using synthetic data")
                training_data = self.generate_synthetic_data()
            
            # Prepare features
            features_df = self.prepare_features(training_data)
            
            if features_df.empty:
                logger.error("Failed to prepare features")
                return False
            
            # Feature columns for training
            feature_cols = ['purchase_count', 'cart_count', 'avg_order_value', 
                          'session_duration', 'cart_to_purchase_ratio', 'total_value']
            
            X = features_df[feature_cols].fillna(0)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train churn model
            y_churn = features_df['churn']
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y_churn, test_size=0.2, random_state=42
            )
            
            self.churn_model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.churn_model.fit(X_train, y_train)
            
            # Evaluate churn model
            churn_pred = self.churn_model.predict(X_test)
            churn_accuracy = accuracy_score(y_test, churn_pred)
            logger.info(f"Churn model accuracy: {churn_accuracy:.3f}")
            
            # Train spending model
            y_spending = features_df['next_month_spending']
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y_spending, test_size=0.2, random_state=42
            )
            
            self.spending_model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.spending_model.fit(X_train, y_train)
            
            # Evaluate spending model
            spending_pred = self.spending_model.predict(X_test)
            spending_mse = mean_squared_error(y_test, spending_pred)
            logger.info(f"Spending model MSE: {spending_mse:.3f}")
            
            self.is_trained = True
            self.save_models()
            
            logger.info("Model training completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Model training error: {e}")
            return False
    
    def load_training_data(self):
        """Load training data from database and CSV files"""
        try:
            # Try to load from database first
            db_data = get_user_behavior_data()
            
            # Try to load from CSV file
            csv_path = "data/user_behavior_training.csv"
            if os.path.exists(csv_path):
                csv_data = pd.read_csv(csv_path)
                if not db_data.empty:
                    return pd.concat([db_data, csv_data], ignore_index=True)
                else:
                    return csv_data
            
            return db_data
            
        except Exception as e:
            logger.error(f"Error loading training data: {e}")
            return pd.DataFrame()
    
    def generate_synthetic_data(self, n_users=1000):
        """Generate synthetic training data for demonstration"""
        logger.info("Generating synthetic training data...")
        
        np.random.seed(42)
        
        data = []
        for user_id in range(1, n_users + 1):
            # Generate user behavior patterns
            purchase_count = np.random.poisson(5)
            cart_count = purchase_count + np.random.poisson(3)
            avg_order_value = np.random.normal(150, 50)
            session_duration = np.random.normal(20, 10)
            
            data.append({
                'user_id': user_id,
                'action': 'purchase',
                'product_id': np.random.randint(1, 11),
                'session_duration': max(1, session_duration),
                'purchase_count': max(0, purchase_count),
                'cart_count': max(0, cart_count),
                'avg_order_value': max(10, avg_order_value)
            })
        
        return pd.DataFrame(data)
    
    def predict_user_behavior(self, user_id):
        """Predict churn probability and spending for a user"""
        try:
            if not self.is_trained:
                logger.warning("Models not trained, loading from file...")
                if not self.load_models():
                    logger.error("Failed to load models")
                    return {"error": "Models not available"}
            
            # Get user behavior data
            user_data = get_user_behavior_data()
            
            if user_data.empty:
                logger.warning("No user data available, using default values")
                # Use default values for new user
                features = np.array([[0, 0, 100, 15, 1, 0]])  # Default user profile
            else:
                user_features = self.prepare_features(user_data)
                
                if user_id in user_features.index:
                    user_row = user_features.loc[user_id]
                else:
                    # Use average values for unknown user
                    user_row = user_features.mean()
                
                feature_cols = ['purchase_count', 'cart_count', 'avg_order_value', 
                              'session_duration', 'cart_to_purchase_ratio', 'total_value']
                features = user_row[feature_cols].values.reshape(1, -1)
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Make predictions
            churn_prob = self.churn_model.predict_proba(features_scaled)[0][1]
            spending_pred = max(0, self.spending_model.predict(features_scaled)[0])
            
            return {
                "churn_probability": float(churn_prob),
                "predicted_spending": float(spending_pred)
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {"error": str(e)}
    
    def save_models(self):
        """Save trained models to disk"""
        try:
            os.makedirs("models", exist_ok=True)
            
            with open("models/churn_model.pkl", "wb") as f:
                pickle.dump(self.churn_model, f)
            
            with open("models/spending_model.pkl", "wb") as f:
                pickle.dump(self.spending_model, f)
            
            with open("models/scaler.pkl", "wb") as f:
                pickle.dump(self.scaler, f)
            
            logger.info("Models saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    def load_models(self):
        """Load trained models from disk"""
        try:
            if (os.path.exists("models/churn_model.pkl") and 
                os.path.exists("models/spending_model.pkl") and 
                os.path.exists("models/scaler.pkl")):
                
                with open("models/churn_model.pkl", "rb") as f:
                    self.churn_model = pickle.load(f)
                
                with open("models/spending_model.pkl", "rb") as f:
                    self.spending_model = pickle.load(f)
                
                with open("models/scaler.pkl", "rb") as f:
                    self.scaler = pickle.load(f)
                
                self.is_trained = True
                logger.info("Models loaded successfully")
                return True
            else:
                logger.warning("Model files not found, training new models...")
                return self.train_models()
                
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False

# Global model instance
_model_instance = None

def get_model_instance():
    """Get or create model instance"""
    global _model_instance
    if _model_instance is None:
        _model_instance = UserBehaviorPredictor()
        if not _model_instance.load_models():
            logger.error("Failed to initialize ML models")
    return _model_instance

def load_user_behavior_model():
    """Load or train user behavior prediction model"""
    return get_model_instance()

def predict_user_behavior(user_id):
    """Predict user behavior using trained models"""
    model = get_model_instance()
    return model.predict_user_behavior(user_id)

def retrain_models():
    """Retrain models with latest data"""
    model = get_model_instance()
    return model.train_models()
