"""
Real-time ML Model Retraining System

This module implements automatic model retraining based on new user behavior data.
It monitors user interactions and triggers retraining when sufficient new data is available.

Features:
- Automatic data collection monitoring
- Incremental model updates
- Performance tracking and validation
- Rollback capability for poor performing models
- Configurable retraining triggers

Author: AI E-Commerce Platform Team
Version: 1.0.0
"""

import os
import time
import logging
import threading
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pickle
import json
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.model_selection import train_test_split

from database import get_connection
from ml_models import UserBehaviorPredictor

# Configure logging for retraining operations
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RealtimeModelRetrainer:
    """
    Real-time model retraining system that monitors user data and updates ML models.
    
    This class manages the entire retraining pipeline including:
    - Data monitoring and collection
    - Model performance tracking
    - Automatic retraining triggers
    - Model validation and deployment
    - Rollback mechanisms for failed updates
    """
    
    def __init__(self, 
                 min_new_samples: int = 100,
                 retrain_interval_hours: int = 24,
                 performance_threshold: float = 0.05,
                 backup_models: bool = True):
        """
        Initialize the real-time retraining system.
        
        Args:
            min_new_samples: Minimum new samples needed to trigger retraining
            retrain_interval_hours: Hours between automatic retraining checks
            performance_threshold: Minimum performance improvement required
            backup_models: Whether to backup models before updating
        """
        self.min_new_samples = min_new_samples
        self.retrain_interval_hours = retrain_interval_hours
        self.performance_threshold = performance_threshold
        self.backup_models = backup_models
        
        # Initialize model predictor
        self.predictor = UserBehaviorPredictor()
        
        # Performance tracking
        self.performance_history = []
        self.last_retrain_time = datetime.now()
        
        # Threading control
        self.running = False
        self.retrain_thread = None
        
        # Model backup directory
        self.backup_dir = "model_backups"
        os.makedirs(self.backup_dir, exist_ok=True)
        
        logger.info("Real-time model retrainer initialized")
    
    def start_monitoring(self):
        """Start the real-time monitoring and retraining service."""
        if self.running:
            logger.warning("Retraining service already running")
            return
        
        self.running = True
        self.retrain_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.retrain_thread.start()
        logger.info("Real-time retraining service started")
    
    def stop_monitoring(self):
        """Stop the real-time monitoring service."""
        self.running = False
        if self.retrain_thread:
            self.retrain_thread.join(timeout=5)
        logger.info("Real-time retraining service stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop that checks for retraining conditions."""
        while self.running:
            try:
                # Check if retraining is needed
                if self._should_retrain():
                    logger.info("Retraining conditions met, starting model update")
                    self.retrain_models()
                
                # Sleep for monitoring interval (check every hour)
                time.sleep(3600)  # 1 hour
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(300)  # Wait 5 minutes before retry
    
    def _should_retrain(self) -> bool:
        """
        Determine if models should be retrained based on various conditions.
        
        Returns:
            bool: True if retraining should be triggered
        """
        # Check time since last retrain
        time_since_retrain = datetime.now() - self.last_retrain_time
        if time_since_retrain.total_seconds() < self.retrain_interval_hours * 3600:
            return False
        
        # Check for sufficient new data
        new_samples = self._count_new_samples()
        if new_samples < self.min_new_samples:
            logger.info(f"Only {new_samples} new samples, need {self.min_new_samples}")
            return False
        
        # Check model performance degradation
        if self._detect_performance_drift():
            logger.info("Performance drift detected, triggering retraining")
            return True
        
        logger.info(f"Sufficient new data ({new_samples} samples), triggering retraining")
        return True
    
    def _count_new_samples(self) -> int:
        """Count new user behavior samples since last retraining."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Count samples added since last retrain
            cursor.execute("""
                SELECT COUNT(*) FROM user_behaviors 
                WHERE created_at > ?
            """, (self.last_retrain_time,))
            
            count = cursor.fetchone()[0]
            conn.close()
            return count
            
        except Exception as e:
            logger.error(f"Error counting new samples: {e}")
            return 0
    
    def _detect_performance_drift(self) -> bool:
        """
        Detect if model performance has degraded significantly.
        
        Returns:
            bool: True if performance drift is detected
        """
        try:
            # Get recent predictions and actual outcomes
            recent_data = self._get_recent_validation_data()
            if len(recent_data) < 50:  # Need minimum samples for validation
                return False
            
            # Calculate current model performance
            current_performance = self._evaluate_current_performance(recent_data)
            
            # Compare with historical performance
            if len(self.performance_history) > 0:
                avg_historical = np.mean([p['accuracy'] for p in self.performance_history[-5:]])
                if current_performance < avg_historical - self.performance_threshold:
                    logger.warning(f"Performance drift detected: {current_performance:.3f} vs {avg_historical:.3f}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error detecting performance drift: {e}")
            return False
    
    def _get_recent_validation_data(self) -> pd.DataFrame:
        """Get recent user behavior data for validation."""
        try:
            conn = get_connection()
            
            # Get recent data with actual outcomes
            query = """
                SELECT user_id, action, session_duration, product_id,
                       CASE WHEN action = 'purchase' THEN 1 ELSE 0 END as converted
                FROM user_behaviors 
                WHERE created_at > ? 
                ORDER BY created_at DESC
                LIMIT 1000
            """
            
            cutoff_time = datetime.now() - timedelta(days=7)
            df = pd.read_sql_query(query, conn, params=(cutoff_time,))
            conn.close()
            
            return df
            
        except Exception as e:
            logger.error(f"Error getting validation data: {e}")
            return pd.DataFrame()
    
    def _evaluate_current_performance(self, data: pd.DataFrame) -> float:
        """Evaluate current model performance on recent data."""
        try:
            if len(data) < 10:
                return 0.0
            
            # Prepare features (simplified for this example)
            features = data[['session_duration']].fillna(0)
            targets = data['converted']
            
            # Get predictions from current model
            if hasattr(self.predictor, 'churn_model') and self.predictor.churn_model:
                predictions = self.predictor.churn_model.predict(features)
                accuracy = accuracy_score(targets, predictions > 0.5)
                return accuracy
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Error evaluating performance: {e}")
            return 0.0
    
    def retrain_models(self) -> bool:
        """
        Retrain ML models with latest data.
        
        Returns:
            bool: True if retraining was successful
        """
        try:
            logger.info("Starting model retraining process")
            
            # Backup current models if enabled
            if self.backup_models:
                self._backup_current_models()
            
            # Load latest training data
            training_data = self._load_latest_training_data()
            if len(training_data) < 100:
                logger.warning("Insufficient training data for retraining")
                return False
            
            # Train new models
            old_performance = self._get_current_model_performance()
            success = self._train_new_models(training_data)
            
            if success:
                # Validate new models
                new_performance = self._validate_new_models(training_data)
                
                # Check if new models are better
                if self._should_deploy_new_models(old_performance, new_performance):
                    self._deploy_new_models()
                    self._update_performance_history(new_performance)
                    self.last_retrain_time = datetime.now()
                    logger.info("Model retraining completed successfully")
                    return True
                else:
                    logger.warning("New models don't meet performance criteria, reverting")
                    self._revert_to_backup()
                    return False
            
            return False
            
        except Exception as e:
            logger.error(f"Error during model retraining: {e}")
            return False
    
    def _backup_current_models(self):
        """Backup current models before retraining."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"models_{timestamp}")
            os.makedirs(backup_path, exist_ok=True)
            
            # Copy current model files
            import shutil
            model_files = ['churn_model.pkl', 'spending_model.pkl', 'scaler.pkl']
            
            for model_file in model_files:
                src_path = os.path.join('models', model_file)
                if os.path.exists(src_path):
                    dst_path = os.path.join(backup_path, model_file)
                    shutil.copy2(src_path, dst_path)
            
            logger.info(f"Models backed up to {backup_path}")
            
        except Exception as e:
            logger.error(f"Error backing up models: {e}")
    
    def _load_latest_training_data(self) -> pd.DataFrame:
        """Load the latest training data including recent user behaviors."""
        try:
            conn = get_connection()
            
            # Comprehensive query to get all user behavior data
            query = """
                SELECT 
                    ub.user_id,
                    ub.action,
                    ub.session_duration,
                    ub.product_id,
                    ub.created_at,
                    COUNT(CASE WHEN ub2.action = 'purchase' THEN 1 END) as purchase_count,
                    COUNT(CASE WHEN ub2.action = 'cart_add' THEN 1 END) as cart_adds,
                    COUNT(CASE WHEN ub2.action = 'view' THEN 1 END) as page_views,
                    AVG(ub2.session_duration) as avg_session_duration
                FROM user_behaviors ub
                LEFT JOIN user_behaviors ub2 ON ub.user_id = ub2.user_id 
                    AND ub2.created_at <= ub.created_at
                GROUP BY ub.user_id, ub.action, ub.session_duration, ub.product_id, ub.created_at
                ORDER BY ub.created_at DESC
                LIMIT 10000
            """
            
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            logger.info(f"Loaded {len(df)} training samples")
            return df
            
        except Exception as e:
            logger.error(f"Error loading training data: {e}")
            return pd.DataFrame()
    
    def _train_new_models(self, training_data: pd.DataFrame) -> bool:
        """Train new ML models with the latest data."""
        try:
            # Create new predictor instance for training
            new_predictor = UserBehaviorPredictor()
            
            # Prepare training data
            features_df = self._prepare_features(training_data)
            if len(features_df) < 50:
                logger.warning("Insufficient prepared features for training")
                return False
            
            # Train models
            success = new_predictor.train_models_with_data(features_df)
            
            if success:
                # Save new models to temporary location
                self._save_temp_models(new_predictor)
                logger.info("New models trained successfully")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error training new models: {e}")
            return False
    
    def _prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for model training."""
        try:
            # Create feature engineering similar to original training
            features = data.copy()
            
            # Fill missing values
            features['session_duration'] = features['session_duration'].fillna(0)
            features['purchase_count'] = features['purchase_count'].fillna(0)
            features['cart_adds'] = features['cart_adds'].fillna(0)
            features['page_views'] = features['page_views'].fillna(0)
            features['avg_session_duration'] = features['avg_session_duration'].fillna(0)
            
            # Create target variables
            features['will_churn'] = (features['purchase_count'] == 0).astype(int)
            features['spending_score'] = np.clip(features['purchase_count'] * 100, 0, 1000)
            
            # Select final features
            feature_columns = [
                'session_duration', 'purchase_count', 'cart_adds', 
                'page_views', 'avg_session_duration', 'will_churn', 'spending_score'
            ]
            
            return features[feature_columns].dropna()
            
        except Exception as e:
            logger.error(f"Error preparing features: {e}")
            return pd.DataFrame()
    
    def _save_temp_models(self, predictor: UserBehaviorPredictor):
        """Save newly trained models to temporary location."""
        try:
            temp_dir = "temp_models"
            os.makedirs(temp_dir, exist_ok=True)
            
            # Save models to temp directory
            if predictor.churn_model:
                with open(os.path.join(temp_dir, 'churn_model.pkl'), 'wb') as f:
                    pickle.dump(predictor.churn_model, f)
            
            if predictor.spending_model:
                with open(os.path.join(temp_dir, 'spending_model.pkl'), 'wb') as f:
                    pickle.dump(predictor.spending_model, f)
            
            if predictor.scaler:
                with open(os.path.join(temp_dir, 'scaler.pkl'), 'wb') as f:
                    pickle.dump(predictor.scaler, f)
            
            logger.info("Temporary models saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving temporary models: {e}")
    
    def _get_current_model_performance(self) -> Dict:
        """Get performance metrics of current models."""
        try:
            if len(self.performance_history) > 0:
                return self.performance_history[-1]
            return {'accuracy': 0.5, 'mse': 1000, 'timestamp': datetime.now()}
            
        except Exception as e:
            logger.error(f"Error getting current performance: {e}")
            return {'accuracy': 0.5, 'mse': 1000, 'timestamp': datetime.now()}
    
    def _validate_new_models(self, validation_data: pd.DataFrame) -> Dict:
        """Validate newly trained models."""
        try:
            # Load temporary models
            temp_predictor = self._load_temp_models()
            if not temp_predictor:
                return {'accuracy': 0.0, 'mse': 10000}
            
            # Prepare validation data
            features = self._prepare_features(validation_data)
            if len(features) < 10:
                return {'accuracy': 0.0, 'mse': 10000}
            
            # Split data for validation
            X = features[['session_duration', 'purchase_count', 'cart_adds', 'page_views']]
            y_churn = features['will_churn']
            y_spending = features['spending_score']
            
            X_train, X_test, y_churn_train, y_churn_test = train_test_split(
                X, y_churn, test_size=0.2, random_state=42
            )
            
            # Evaluate churn model
            churn_pred = temp_predictor.churn_model.predict(X_test)
            accuracy = accuracy_score(y_churn_test, churn_pred > 0.5)
            
            # Evaluate spending model
            _, _, y_spending_train, y_spending_test = train_test_split(
                X, y_spending, test_size=0.2, random_state=42
            )
            spending_pred = temp_predictor.spending_model.predict(X_test)
            mse = mean_squared_error(y_spending_test, spending_pred)
            
            performance = {
                'accuracy': accuracy,
                'mse': mse,
                'timestamp': datetime.now(),
                'samples_used': len(X_test)
            }
            
            logger.info(f"New model performance: Accuracy={accuracy:.3f}, MSE={mse:.2f}")
            return performance
            
        except Exception as e:
            logger.error(f"Error validating new models: {e}")
            return {'accuracy': 0.0, 'mse': 10000, 'timestamp': datetime.now()}
    
    def _load_temp_models(self) -> Optional[UserBehaviorPredictor]:
        """Load models from temporary location."""
        try:
            temp_dir = "temp_models"
            predictor = UserBehaviorPredictor()
            
            # Load models
            churn_path = os.path.join(temp_dir, 'churn_model.pkl')
            if os.path.exists(churn_path):
                with open(churn_path, 'rb') as f:
                    predictor.churn_model = pickle.load(f)
            
            spending_path = os.path.join(temp_dir, 'spending_model.pkl')
            if os.path.exists(spending_path):
                with open(spending_path, 'rb') as f:
                    predictor.spending_model = pickle.load(f)
            
            scaler_path = os.path.join(temp_dir, 'scaler.pkl')
            if os.path.exists(scaler_path):
                with open(scaler_path, 'rb') as f:
                    predictor.scaler = pickle.load(f)
            
            return predictor
            
        except Exception as e:
            logger.error(f"Error loading temporary models: {e}")
            return None
    
    def _should_deploy_new_models(self, old_perf: Dict, new_perf: Dict) -> bool:
        """Determine if new models should be deployed."""
        try:
            # Check accuracy improvement
            accuracy_improvement = new_perf['accuracy'] - old_perf['accuracy']
            
            # Check MSE improvement (lower is better)
            mse_improvement = old_perf['mse'] - new_perf['mse']
            
            # Deploy if either metric shows significant improvement
            if accuracy_improvement > self.performance_threshold:
                logger.info(f"Accuracy improved by {accuracy_improvement:.3f}")
                return True
            
            if mse_improvement > 100:  # Adjust threshold as needed
                logger.info(f"MSE improved by {mse_improvement:.2f}")
                return True
            
            # Don't deploy if performance is significantly worse
            if accuracy_improvement < -self.performance_threshold:
                logger.warning(f"Accuracy decreased by {abs(accuracy_improvement):.3f}")
                return False
            
            # Deploy if performance is similar but we have more data
            if abs(accuracy_improvement) <= self.performance_threshold:
                logger.info("Performance similar, deploying updated models")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error evaluating deployment decision: {e}")
            return False
    
    def _deploy_new_models(self):
        """Deploy new models to production."""
        try:
            import shutil
            
            temp_dir = "temp_models"
            models_dir = "models"
            
            # Move models from temp to production
            model_files = ['churn_model.pkl', 'spending_model.pkl', 'scaler.pkl']
            
            for model_file in model_files:
                temp_path = os.path.join(temp_dir, model_file)
                prod_path = os.path.join(models_dir, model_file)
                
                if os.path.exists(temp_path):
                    shutil.move(temp_path, prod_path)
            
            # Reload models in the main predictor
            self.predictor.load_models()
            
            logger.info("New models deployed successfully")
            
        except Exception as e:
            logger.error(f"Error deploying new models: {e}")
    
    def _revert_to_backup(self):
        """Revert to the most recent backup if new models fail."""
        try:
            # Find most recent backup
            backup_dirs = [d for d in os.listdir(self.backup_dir) if d.startswith('models_')]
            if not backup_dirs:
                logger.error("No backup models found for revert")
                return
            
            latest_backup = sorted(backup_dirs)[-1]
            backup_path = os.path.join(self.backup_dir, latest_backup)
            
            # Restore models from backup
            import shutil
            model_files = ['churn_model.pkl', 'spending_model.pkl', 'scaler.pkl']
            
            for model_file in model_files:
                backup_file = os.path.join(backup_path, model_file)
                prod_file = os.path.join('models', model_file)
                
                if os.path.exists(backup_file):
                    shutil.copy2(backup_file, prod_file)
            
            # Reload original models
            self.predictor.load_models()
            
            logger.info(f"Reverted to backup models from {latest_backup}")
            
        except Exception as e:
            logger.error(f"Error reverting to backup: {e}")
    
    def _update_performance_history(self, performance: Dict):
        """Update performance history with new metrics."""
        self.performance_history.append(performance)
        
        # Keep only last 50 performance records
        if len(self.performance_history) > 50:
            self.performance_history = self.performance_history[-50:]
        
        # Save performance history to file
        try:
            with open('performance_history.json', 'w') as f:
                # Convert datetime objects to strings for JSON serialization
                history_for_json = []
                for perf in self.performance_history:
                    perf_copy = perf.copy()
                    perf_copy['timestamp'] = perf_copy['timestamp'].isoformat()
                    history_for_json.append(perf_copy)
                
                json.dump(history_for_json, f, indent=2)
            
            logger.info("Performance history updated")
            
        except Exception as e:
            logger.error(f"Error saving performance history: {e}")
    
    def get_retraining_status(self) -> Dict:
        """Get current status of the retraining system."""
        return {
            'running': self.running,
            'last_retrain': self.last_retrain_time.isoformat(),
            'new_samples': self._count_new_samples(),
            'min_samples_needed': self.min_new_samples,
            'performance_history_length': len(self.performance_history),
            'next_check_in_hours': self.retrain_interval_hours
        }
    
    def force_retrain(self) -> bool:
        """Force immediate model retraining regardless of conditions."""
        logger.info("Forcing immediate model retraining")
        return self.retrain_models()


# Global retrainer instance
_retrainer = None

def get_retrainer() -> RealtimeModelRetrainer:
    """Get or create global retrainer instance."""
    global _retrainer
    if _retrainer is None:
        _retrainer = RealtimeModelRetrainer()
    return _retrainer

def start_retraining_service():
    """Start the real-time retraining service."""
    retrainer = get_retrainer()
    retrainer.start_monitoring()
    return retrainer

def stop_retraining_service():
    """Stop the real-time retraining service."""
    global _retrainer
    if _retrainer:
        _retrainer.stop_monitoring()

if __name__ == "__main__":
    # Start retraining service for testing
    logger.info("Starting real-time model retraining service")
    retrainer = start_retraining_service()
    
    try:
        # Keep service running
        while True:
            time.sleep(60)
            status = retrainer.get_retraining_status()
            logger.info(f"Retraining status: {status}")
    except KeyboardInterrupt:
        logger.info("Shutting down retraining service")
        stop_retraining_service()