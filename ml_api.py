from flask import Flask, request, jsonify
import logging
from ml_models import predict_user_behavior, retrain_models
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "ML API"})

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
