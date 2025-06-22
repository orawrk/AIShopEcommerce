"""
Machine Learning API for AI-powered e-commerce platform.

This Flask-based API service provides machine learning capabilities including:
- User behavior prediction (churn and spending patterns)
- Model retraining with latest data
- Model health monitoring and status checks

The API integrates with the main e-commerce platform to provide:
- Real-time user behavior analytics
- Predictive insights for business intelligence
- Automated model maintenance and updates

Author: AI E-Commerce Platform Team
Version: 1.0.0
Port: 8000
"""

from flask import Flask, request, jsonify
import logging
from ml_models import predict_user_behavior, retrain_models
from ml_retraining import get_retrainer, start_retraining_service, stop_retraining_service
import os
import threading

# Configure comprehensive logging for ML operations
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask application for ML API
app = Flask(__name__)

# Global retrainer instance
retrainer_instance = None
retrainer_lock = threading.Lock()

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring ML API status.
    
    This endpoint is used by:
    - Load balancers for health checks
    - Monitoring systems for service status
    - Integration tests for API availability
    
    Returns:
        JSON response with service health status
    """
    return jsonify({
        "status": "healthy", 
        "service": "ML API",
        "version": "1.0.0",
        "capabilities": ["churn_prediction", "spending_prediction", "model_retraining"]
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict user behavior (churn and spending)"""
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data:
            return jsonify({"error": "user_id is required"}), 400
        
        user_id = data['user_id']
        
        # Get predictions
        predictions = predict_user_behavior(user_id)
        
        if "error" in predictions:
            return jsonify(predictions), 500
        
        logger.info(f"Prediction successful for user {user_id}")
        return jsonify(predictions)
        
    except Exception as e:
        logger.error(f"Prediction endpoint error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/retrain', methods=['POST'])
def retrain():
    """Retrain ML models with latest data"""
    try:
        logger.info("Starting model retraining...")
        
        success = retrain_models()
        
        if success:
            logger.info("Model retraining completed successfully")
            return jsonify({"message": "Models retrained successfully"})
        else:
            logger.error("Model retraining failed")
            return jsonify({"error": "Failed to retrain models"}), 500
            
    except Exception as e:
        logger.error(f"Retrain endpoint error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/model-info', methods=['GET'])
def model_info():
    """Get information about the trained models"""
    try:
        # Return basic model information
        info = {
            "models": ["churn_prediction", "spending_prediction"],
            "algorithm": "Random Forest",
            "features": [
                "purchase_count",
                "cart_count", 
                "avg_order_value",
                "session_duration",
                "cart_to_purchase_ratio",
                "total_value"
            ],
            "targets": [
                "churn_probability",
                "predicted_spending"
            ]
        }
        
        return jsonify(info)
        
    except Exception as e:
        logger.error(f"Model info endpoint error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/retraining/status', methods=['GET'])
def get_retraining_status():
    """Get current status of the real-time retraining system"""
    try:
        global retrainer_instance
        with retrainer_lock:
            if retrainer_instance is None:
                retrainer_instance = get_retrainer()
            
            status = retrainer_instance.get_retraining_status()
            return jsonify({
                "status": "success",
                "retraining": status
            })
    except Exception as e:
        logger.error(f"Error getting retraining status: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/retraining/start', methods=['POST'])
def start_retraining():
    """Start the real-time retraining service"""
    try:
        global retrainer_instance
        with retrainer_lock:
            if retrainer_instance is None:
                retrainer_instance = start_retraining_service()
            else:
                retrainer_instance.start_monitoring()
            
            return jsonify({
                "status": "success",
                "message": "Real-time retraining service started"
            })
    except Exception as e:
        logger.error(f"Error starting retraining service: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/retraining/stop', methods=['POST'])
def stop_retraining():
    """Stop the real-time retraining service"""
    try:
        global retrainer_instance
        with retrainer_lock:
            if retrainer_instance:
                retrainer_instance.stop_monitoring()
            
            return jsonify({
                "status": "success",
                "message": "Real-time retraining service stopped"
            })
    except Exception as e:
        logger.error(f"Error stopping retraining service: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/retraining/force', methods=['POST'])
def force_retraining():
    """Force immediate model retraining"""
    try:
        global retrainer_instance
        with retrainer_lock:
            if retrainer_instance is None:
                retrainer_instance = get_retrainer()
            
            success = retrainer_instance.force_retrain()
            
            if success:
                return jsonify({
                    "status": "success",
                    "message": "Model retraining completed successfully"
                })
            else:
                return jsonify({
                    "status": "failed",
                    "message": "Model retraining failed"
                }), 500
    except Exception as e:
        logger.error(f"Error forcing retraining: {e}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info("Starting ML API server...")
    
    # Initialize models on startup
    try:
        from ml_models import get_model_instance
        model = get_model_instance()
        logger.info("ML models initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize ML models: {e}")
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=False
    )
