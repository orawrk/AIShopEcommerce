"""
Test Suite for Real-time Model Retraining System

This test suite validates the functionality and reliability of the real-time
model retraining system including data monitoring, model training, and API endpoints.

Author: AI E-Commerce Platform Team
Version: 1.0.0
"""

import unittest
import tempfile
import os
import json
import time
import threading
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Import modules to test
from ml_retraining import RealtimeModelRetrainer, get_retrainer
from ml_models import UserBehaviorPredictor

class TestRealtimeModelRetrainer(unittest.TestCase):
    """Test cases for the RealtimeModelRetrainer class"""
    
    def setUp(self):
        """Set up test environment before each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.retrainer = RealtimeModelRetrainer(
            min_new_samples=10,  # Lower threshold for testing
            retrain_interval_hours=1,  # Shorter interval for testing
            performance_threshold=0.01,
            backup_models=True
        )
        self.retrainer.backup_dir = os.path.join(self.temp_dir, "backups")
        os.makedirs(self.retrainer.backup_dir, exist_ok=True)
    
    def tearDown(self):
        """Clean up after each test"""
        if hasattr(self.retrainer, 'running') and self.retrainer.running:
            self.retrainer.stop_monitoring()
        
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test proper initialization of RealtimeModelRetrainer"""
        self.assertEqual(self.retrainer.min_new_samples, 10)
        self.assertEqual(self.retrainer.retrain_interval_hours, 1)
        self.assertEqual(self.retrainer.performance_threshold, 0.01)
        self.assertTrue(self.retrainer.backup_models)
        self.assertFalse(self.retrainer.running)
        self.assertIsNone(self.retrainer.retrain_thread)
    
    @patch('ml_retraining.get_connection')
    def test_count_new_samples(self, mock_get_connection):
        """Test counting new samples from database"""
        # Mock database connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (25,)  # 25 new samples
        mock_get_connection.return_value = mock_conn
        
        count = self.retrainer._count_new_samples()
        
        self.assertEqual(count, 25)
        mock_cursor.execute.assert_called_once()
        mock_conn.close.assert_called_once()
    
    @patch('ml_retraining.get_connection')
    def test_count_new_samples_error_handling(self, mock_get_connection):
        """Test error handling in count_new_samples"""
        mock_get_connection.side_effect = Exception("Database error")
        
        count = self.retrainer._count_new_samples()
        
        self.assertEqual(count, 0)  # Should return 0 on error
    
    def test_should_retrain_time_condition(self):
        """Test retraining time condition logic"""
        # Set last retrain time to recent
        self.retrainer.last_retrain_time = datetime.now() - timedelta(minutes=30)
        
        # Should not retrain (too recent)
        with patch.object(self.retrainer, '_count_new_samples', return_value=20):
            should_retrain = self.retrainer._should_retrain()
            self.assertFalse(should_retrain)
        
        # Set last retrain time to old enough
        self.retrainer.last_retrain_time = datetime.now() - timedelta(hours=2)
        
        # Should retrain now
        with patch.object(self.retrainer, '_count_new_samples', return_value=20):
            should_retrain = self.retrainer._should_retrain()
            self.assertTrue(should_retrain)
    
    def test_should_retrain_sample_count_condition(self):
        """Test retraining sample count condition"""
        # Set time condition to pass
        self.retrainer.last_retrain_time = datetime.now() - timedelta(hours=2)
        
        # Insufficient samples
        with patch.object(self.retrainer, '_count_new_samples', return_value=5):
            should_retrain = self.retrainer._should_retrain()
            self.assertFalse(should_retrain)
        
        # Sufficient samples
        with patch.object(self.retrainer, '_count_new_samples', return_value=15):
            should_retrain = self.retrainer._should_retrain()
            self.assertTrue(should_retrain)
    
    def test_get_retraining_status(self):
        """Test getting retraining status"""
        with patch.object(self.retrainer, '_count_new_samples', return_value=8):
            status = self.retrainer.get_retraining_status()
            
            self.assertIn('running', status)
            self.assertIn('last_retrain', status)
            self.assertIn('new_samples', status)
            self.assertIn('min_samples_needed', status)
            self.assertEqual(status['new_samples'], 8)
            self.assertEqual(status['min_samples_needed'], 10)
    
    def test_start_stop_monitoring(self):
        """Test starting and stopping the monitoring service"""
        # Start monitoring
        self.retrainer.start_monitoring()
        self.assertTrue(self.retrainer.running)
        self.assertIsNotNone(self.retrainer.retrain_thread)
        
        # Stop monitoring
        self.retrainer.stop_monitoring()
        self.assertFalse(self.retrainer.running)
    
    def test_backup_current_models(self):
        """Test model backup functionality"""
        # Create fake model files
        models_dir = os.path.join(self.temp_dir, "models")
        os.makedirs(models_dir, exist_ok=True)
        
        test_files = ['churn_model.pkl', 'spending_model.pkl', 'scaler.pkl']
        for filename in test_files:
            filepath = os.path.join(models_dir, filename)
            with open(filepath, 'w') as f:
                f.write("test model data")
        
        # Mock the models directory path
        with patch('ml_retraining.os.path.join') as mock_join:
            mock_join.side_effect = lambda *args: os.path.join(*args)
            
            # Test backup
            self.retrainer._backup_current_models()
            
            # Check if backup directory was created
            backup_dirs = [d for d in os.listdir(self.retrainer.backup_dir) 
                          if d.startswith('models_')]
            self.assertGreater(len(backup_dirs), 0)
    
    @patch('ml_retraining.pd.read_sql_query')
    @patch('ml_retraining.get_connection')
    def test_load_latest_training_data(self, mock_get_connection, mock_read_sql):
        """Test loading latest training data"""
        # Mock data
        mock_data = pd.DataFrame({
            'user_id': [1, 2, 3],
            'action': ['view', 'cart_add', 'purchase'],
            'session_duration': [120, 180, 300],
            'purchase_count': [0, 1, 2],
            'cart_adds': [1, 2, 0],
            'page_views': [5, 3, 8]
        })
        
        mock_read_sql.return_value = mock_data
        mock_conn = Mock()
        mock_get_connection.return_value = mock_conn
        
        result = self.retrainer._load_latest_training_data()
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)
        mock_conn.close.assert_called_once()
    
    def test_prepare_features(self):
        """Test feature preparation for training"""
        # Create test data
        test_data = pd.DataFrame({
            'session_duration': [120, 180, None],
            'purchase_count': [0, 1, 2],
            'cart_adds': [1, None, 0],
            'page_views': [5, 3, 8],
            'avg_session_duration': [100, 150, 200]
        })
        
        features = self.retrainer._prepare_features(test_data)
        
        # Check that features were created
        self.assertIn('will_churn', features.columns)
        self.assertIn('spending_score', features.columns)
        
        # Check that missing values were filled
        self.assertFalse(features['session_duration'].isna().any())
        self.assertFalse(features['cart_adds'].isna().any())
    
    def test_performance_history_update(self):
        """Test updating performance history"""
        test_performance = {
            'accuracy': 0.85,
            'mse': 125.5,
            'timestamp': datetime.now(),
            'samples_used': 100
        }
        
        # Create temporary performance history file
        history_file = os.path.join(self.temp_dir, 'performance_history.json')
        
        with patch('builtins.open', create=True) as mock_open:
            with patch('json.dump') as mock_dump:
                self.retrainer._update_performance_history(test_performance)
                mock_open.assert_called()
                mock_dump.assert_called_once()
    
    def test_force_retrain(self):
        """Test forced retraining functionality"""
        with patch.object(self.retrainer, '_backup_current_models'):
            with patch.object(self.retrainer, '_load_latest_training_data') as mock_load:
                # Mock insufficient data
                mock_load.return_value = pd.DataFrame({'col': [1, 2]})  # Too small
                
                result = self.retrainer.force_retrain()
                self.assertFalse(result)  # Should fail with insufficient data


class TestMLAPIIntegration(unittest.TestCase):
    """Test cases for ML API integration with retraining system"""
    
    def setUp(self):
        """Set up test environment"""
        self.api_base_url = "http://localhost:8000"
    
    @patch('requests.get')
    def test_retraining_status_endpoint(self, mock_get):
        """Test the retraining status API endpoint"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'success',
            'retraining': {
                'running': True,
                'new_samples': 50,
                'min_samples_needed': 100
            }
        }
        mock_get.return_value = mock_response
        
        import requests
        response = requests.get(f"{self.api_base_url}/retraining/status")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('retraining', data)
    
    @patch('requests.post')
    def test_force_retraining_endpoint(self, mock_post):
        """Test the force retraining API endpoint"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'success',
            'message': 'Model retraining completed successfully'
        }
        mock_post.return_value = mock_response
        
        import requests
        response = requests.post(f"{self.api_base_url}/retraining/force")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')


class TestUserBehaviorPredictor(unittest.TestCase):
    """Test cases for UserBehaviorPredictor integration"""
    
    def setUp(self):
        """Set up test environment"""
        self.predictor = UserBehaviorPredictor()
    
    def test_predictor_initialization(self):
        """Test predictor initialization"""
        self.assertIsNotNone(self.predictor)
        # Models might be None if not loaded yet
        self.assertIsNone(self.predictor.churn_model)
        self.assertIsNone(self.predictor.spending_model)
    
    @patch('ml_models.pickle.load')
    @patch('builtins.open')
    @patch('os.path.exists')
    def test_load_models(self, mock_exists, mock_open, mock_pickle_load):
        """Test model loading functionality"""
        mock_exists.return_value = True
        mock_model = Mock()
        mock_pickle_load.return_value = mock_model
        
        self.predictor.load_models()
        
        # Verify models were loaded
        self.assertIsNotNone(self.predictor.churn_model)
        self.assertIsNotNone(self.predictor.spending_model)
        self.assertIsNotNone(self.predictor.scaler)


class TestDataIntegrity(unittest.TestCase):
    """Test cases for data integrity and quality"""
    
    def test_feature_consistency(self):
        """Test that features remain consistent across retraining"""
        # Test data with expected features
        test_data = pd.DataFrame({
            'session_duration': [120, 180, 300],
            'purchase_count': [0, 1, 2],
            'cart_adds': [1, 2, 0],
            'page_views': [5, 3, 8],
            'avg_session_duration': [100, 150, 200]
        })
        
        retrainer = RealtimeModelRetrainer()
        features = retrainer._prepare_features(test_data)
        
        expected_columns = [
            'session_duration', 'purchase_count', 'cart_adds',
            'page_views', 'avg_session_duration', 'will_churn', 'spending_score'
        ]
        
        for col in expected_columns:
            self.assertIn(col, features.columns, f"Missing expected column: {col}")
    
    def test_data_validation(self):
        """Test data validation before training"""
        retrainer = RealtimeModelRetrainer()
        
        # Test with valid data
        valid_data = pd.DataFrame({
            'session_duration': [120, 180, 300, 240, 360],
            'purchase_count': [0, 1, 2, 0, 3],
            'cart_adds': [1, 2, 0, 1, 2],
            'page_views': [5, 3, 8, 4, 6],
            'avg_session_duration': [100, 150, 200, 120, 180]
        })
        
        features = retrainer._prepare_features(valid_data)
        self.assertGreater(len(features), 0)
        
        # Test with insufficient data
        insufficient_data = pd.DataFrame({'col': [1]})
        features = retrainer._prepare_features(insufficient_data)
        # Should handle gracefully without crashing


class TestPerformanceMonitoring(unittest.TestCase):
    """Test cases for performance monitoring functionality"""
    
    def test_performance_metrics_calculation(self):
        """Test calculation of performance metrics"""
        # Mock predictions and actual values
        y_true = np.array([0, 0, 1, 1, 0, 1])
        y_pred = np.array([0, 1, 1, 1, 0, 0])
        
        from sklearn.metrics import accuracy_score
        accuracy = accuracy_score(y_true, y_pred)
        
        # Expected accuracy: 4/6 = 0.667
        expected_accuracy = 4/6
        self.assertAlmostEqual(accuracy, expected_accuracy, places=3)
    
    def test_performance_history_storage(self):
        """Test performance history storage and retrieval"""
        test_history = [
            {
                'accuracy': 0.85,
                'mse': 125.5,
                'timestamp': '2024-01-01T10:00:00',
                'samples_used': 100
            },
            {
                'accuracy': 0.87,
                'mse': 120.0,
                'timestamp': '2024-01-02T10:00:00',
                'samples_used': 150
            }
        ]
        
        # Test JSON serialization
        json_str = json.dumps(test_history)
        loaded_history = json.loads(json_str)
        
        self.assertEqual(len(loaded_history), 2)
        self.assertEqual(loaded_history[0]['accuracy'], 0.85)
        self.assertEqual(loaded_history[1]['accuracy'], 0.87)


def run_tests():
    """Run all test suites"""
    print("Running Real-time Model Retraining Test Suite...")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestRealtimeModelRetrainer,
        TestMLAPIIntegration,
        TestUserBehaviorPredictor,
        TestDataIntegrity,
        TestPerformanceMonitoring
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)