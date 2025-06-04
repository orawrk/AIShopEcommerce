# AI-Powered E-Commerce Platform

A comprehensive full-stack e-commerce platform built with Streamlit, featuring AI-powered customer support using ChatGPT API and machine learning models for user behavior prediction.

## 🚀 Features

### Core E-commerce Functionality
- **Product Catalog**: Browse products with search, filtering, and sorting capabilities
- **Shopping Cart**: Add/remove items, quantity management, and checkout process
- **Order Management**: Track order history and status updates
- **Inventory Management**: Admin dashboard for stock control
- **User Authentication**: Basic user session management

### AI-Powered Features
- **ChatGPT Customer Support**: 24/7 AI assistant for customer inquiries
- **Product Recommendations**: AI-generated personalized product suggestions
- **Customer Sentiment Analysis**: Analyze customer messages for better support
- **Personalized Email Generation**: AI-generated marketing emails

### Machine Learning Analytics
- **Churn Prediction**: Predict likelihood of customer leaving (Random Forest Classifier)
- **Spending Prediction**: Forecast customer monthly spending (Random Forest Regressor)
- **User Behavior Analytics**: Comprehensive dashboard with predictive insights
- **Real-time Predictions**: RESTful API for ML model predictions

## 🛠 Technology Stack

### Frontend
- **Streamlit**: Interactive web application framework
- **Plotly**: Data visualization and charts
- **Pandas**: Data manipulation and analysis

### Backend
- **SQLite**: Database for product catalog, orders, and user behavior
- **Flask**: RESTful API server for ML predictions
- **Python**: Core application logic

### AI & Machine Learning
- **OpenAI GPT-4o**: Customer support chatbot and recommendations
- **Scikit-learn**: Machine learning models (Random Forest)
- **NumPy**: Numerical computing for data processing

### Infrastructure
- **PostgreSQL**: Available for production deployment
- **Replit**: Cloud hosting and development environment

## 📊 Machine Learning Models

### 1. Churn Prediction Model
- **Algorithm**: Random Forest Classifier
- **Purpose**: Predict probability of customer churn
- **Features**: 
  - Purchase count
  - Cart activity
  - Average order value
  - Session duration
  - Cart-to-purchase ratio
  - Total customer value
- **Output**: Churn probability (0-1)

### 2. Spending Prediction Model
- **Algorithm**: Random Forest Regressor
- **Purpose**: Forecast monthly customer spending
- **Features**: Same as churn model
- **Output**: Predicted spending amount ($)

### Training Dataset
The models are trained on comprehensive user behavior data including:
- User purchase history
- Shopping cart interactions
- Session duration metrics
- Product browsing patterns
- Order value trends

Training data is stored in `data/user_behavior_training.csv` with 50+ user records containing realistic e-commerce behavior patterns.

## 🗂 Project Structure

```
├── app.py                          # Main Streamlit application
├── database.py                     # Database operations and setup
├── chatbot.py                      # OpenAI GPT integration
├── ml_models.py                    # Machine learning model implementation
├── ml_api.py                       # Flask API for ML predictions
├── utils.py                        # Utility functions
├── data/
│   ├── sample_products.csv         # Product catalog data
│   └── user_behavior_training.csv  # ML training dataset
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
├── models/                         # Saved ML models (auto-generated)
│   ├── churn_model.pkl
│   ├── spending_model.pkl
│   └── scaler.pkl
└── README.md                       # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- OpenAI API key (for AI features)

### Installation & Setup

1. **Install Dependencies**
   ```bash
   pip install streamlit pandas scikit-learn flask plotly openai requests numpy
   ```

2. **Set Environment Variables**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

3. **Initialize Database**
   The application automatically creates and populates the SQLite database on first run.

4. **Start the Application**
   ```bash
   # Terminal 1: Start Streamlit app
   streamlit run app.py --server.port 5000
   
   # Terminal 2: Start ML API server
   python ml_api.py
   ```

5. **Access the Application**
   - Main App: http://localhost:5000
   - ML API: http://localhost:8000

## 📋 API Endpoints

### ML Prediction API

#### Health Check
```http
GET /health
```

#### User Behavior Prediction
```http
POST /predict
Content-Type: application/json

{
  "user_id": 1
}
```

**Response:**
```json
{
  "churn_probability": 0.23,
  "predicted_spending": 234.56
}
```

#### Model Retraining
```http
POST /retrain
```

#### Model Information
```http
GET /model-info
```

## 🎯 Usage Guide

### Customer Features
1. **Browse Products**: Use search and filters to find items
2. **Shopping Cart**: Add items and proceed to checkout
3. **Order Tracking**: View order history and status
4. **AI Support**: Chat with AI assistant for help

### Admin Features
1. **Inventory Management**: Update product stock levels
2. **User Analytics**: View ML-powered user insights
3. **Order Management**: Monitor order statistics
4. **ML Predictions**: Access churn and spending forecasts

### AI Assistant Commands
- "Track my order" - Get order status information
- "What's your return policy?" - Learn about returns
- "Recommend products" - Get personalized suggestions
- General customer service inquiries

## 🔧 Configuration

### Streamlit Configuration (.streamlit/config.toml)
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
base = "light"
```

### Database Configuration
- SQLite database: `ecommerce.db`
- Auto-initialization with sample data
- PostgreSQL support available for production

## 📊 Business Metrics

The platform tracks key e-commerce metrics:
- **Customer Acquisition**: New user registrations
- **Customer Retention**: Churn rate and repeat purchases
- **Revenue Analytics**: Order values and trends
- **Product Performance**: Best sellers and inventory turnover
- **Customer Engagement**: Session duration and cart abandonment

## 🛡 Error Handling

The application includes comprehensive error handling:
- **Database Failures**: Graceful fallbacks and user notifications
- **API Timeouts**: Retry mechanisms and fallback responses
- **ML Model Issues**: Default predictions when models unavailable
- **User Input Validation**: Sanitization and format checking

## 🚀 Production Deployment

For production deployment:
1. Replace SQLite with PostgreSQL
2. Configure environment variables securely
3. Use production WSGI server (Gunicorn)
4. Implement proper authentication
5. Set up monitoring and logging
6. Configure load balancing for ML API

## 🔮 Future Enhancements

- **Advanced Recommendations**: Collaborative filtering algorithms
- **Real-time Chat**: WebSocket-based customer support
- **Payment Integration**: Stripe/PayPal checkout
- **Mobile App**: React Native companion app
- **Advanced Analytics**: Time-series forecasting
- **A/B Testing**: Feature experimentation framework

## 📄 License

This project is built for educational and demonstration purposes. Please ensure proper licensing for production use.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📞 Support

For technical support or questions about the AI features, please ensure you have:
- Valid OpenAI API key configured
- All dependencies properly installed
- Both Streamlit and Flask servers running

The platform is designed to be robust and user-friendly, with clear error messages and fallback options when external services are unavailable.