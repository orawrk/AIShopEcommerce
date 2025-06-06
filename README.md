# AI-Powered E-Commerce Platform

A comprehensive e-commerce platform built with FastAPI backend, Streamlit frontend, and AI-powered features including ChatGPT integration for customer support and machine learning models for user behavior prediction.

## 🚀 Features

### Core E-Commerce Functionality
- **Product Catalog**: Browse 18+ authentic products across 5 categories (Electronics, Clothing, Books, Home & Garden, Sports)
- **Shopping Cart**: Add, update, and remove items with real-time inventory tracking
- **Order Management**: Complete order processing with automatic status updates
- **Inventory Management**: Real-time stock tracking and updates

### AI-Powered Features
- **ChatGPT Customer Support**: Intelligent chatbot for customer queries and product recommendations
- **Machine Learning Analytics**: User behavior prediction models for churn and spending forecasts
- **Personalized Recommendations**: AI-driven product suggestions based on user preferences
- **Sentiment Analysis**: Customer feedback analysis for improved service

### Technical Architecture
- **FastAPI Backend**: RESTful API with proper MVC architecture
- **PostgreSQL Database**: Robust data storage with authentic product data
- **Streamlit Frontend**: Interactive user interface
- **Docker Support**: Containerized deployment ready
- **ML Models**: Scikit-learn based predictive analytics

## 🛠 Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Primary database
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server

### Frontend
- **Streamlit**: Python-based web application framework
- **Plotly**: Interactive data visualizations
- **Pandas**: Data manipulation and analysis

### AI/ML Components
- **OpenAI GPT**: Customer support chatbot
- **Scikit-learn**: Machine learning models
- **NumPy/Pandas**: Data processing

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-service orchestration

## 📦 Installation

### Prerequisites
- Python 3.11+
- PostgreSQL
- Docker (optional)
- OpenAI API Key

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai-ecommerce-platform
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/ecommerce"
export OPENAI_API_KEY="your-openai-api-key"
```

4. **Initialize database**
```bash
cd backend
python seed_data.py
```

5. **Start the services**
```bash
# Terminal 1 - FastAPI Backend (Port 8001)
cd backend
python main.py

# Terminal 2 - ML API (Port 8000)
python ml_api.py

# Terminal 3 - Streamlit Frontend (Port 5000)
streamlit run app.py --server.port 5000
```

### Docker Deployment

```bash
docker-compose up -d
```

## 🔧 API Endpoints

### Products API
- `GET /api/v1/products/` - List all products with pagination and filtering
- `GET /api/v1/products/{id}` - Get specific product details
- `POST /api/v1/products/` - Create new product (admin)
- `PUT /api/v1/products/{id}` - Update product (admin)
- `DELETE /api/v1/products/{id}` - Delete product (admin)

### Machine Learning API
- `GET /ml/health` - Health check
- `POST /ml/predict` - User behavior prediction
- `POST /ml/retrain` - Retrain models
- `GET /ml/model-info` - Model information

## 📊 Database Schema

### Products Table
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    rating DECIMAL(3,2) NOT NULL DEFAULT 0.0,
    image_url VARCHAR(500),
    sku VARCHAR(100) UNIQUE NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🤖 AI Features

### ChatGPT Integration
The platform includes intelligent customer support powered by OpenAI's GPT models:
- Product recommendations
- Customer query resolution
- Sentiment analysis
- Personalized email generation

### Machine Learning Models
- **Churn Prediction**: Identifies users likely to stop purchasing
- **Spending Prediction**: Forecasts user spending patterns
- **Recommendation Engine**: Suggests relevant products

## 🔒 Environment Variables

```bash
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce
PGHOST=localhost
PGPORT=5432
PGDATABASE=ecommerce
PGUSER=username
PGPASSWORD=password

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Application
DEBUG=True
SECRET_KEY=your-secret-key
```

## 📁 Project Structure

```
ai-ecommerce-platform/
├── backend/                 # FastAPI backend
│   ├── config/             # Configuration files
│   ├── controllers/        # API controllers
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   └── main.py            # FastAPI application
├── data/                   # Sample data files
├── models/                 # Trained ML models
├── app.py                  # Streamlit frontend
├── ml_api.py              # ML API service
├── chatbot.py             # ChatGPT integration
├── database.py            # Database utilities
├── ml_models.py           # ML model training
├── utils.py               # Utility functions
├── docker-compose.yml     # Docker configuration
└── README.md              # This file
```

## 🚀 Deployment

The platform is designed for easy deployment with multiple options:

### Local Development
- Run each service independently
- SQLite for quick testing
- PostgreSQL for production-like environment

### Docker Deployment
- Multi-container setup with Docker Compose
- Includes PostgreSQL, FastAPI, and Streamlit services
- Production-ready configuration

### Cloud Deployment
- Compatible with major cloud providers
- Environment variable configuration
- Scalable architecture

## 🔄 Product Data

The platform includes authentic product data from major brands:

**Electronics**: iPhone 15 Pro, MacBook Air M3, Sony WH-1000XM5, Samsung QLED TV, Nintendo Switch OLED

**Clothing**: Levi's 501 Jeans, Nike Air Force 1, Patagonia Jacket, Uniqlo Heattech

**Books**: The Psychology of Money, Atomic Habits, Sapiens

**Home & Garden**: Dyson V15 Vacuum, Instant Pot, Philips Hue

**Sports**: Hydro Flask, Yeti Tumbler, Theraband Resistance Bands

## 📈 Analytics Dashboard

The admin dashboard provides comprehensive analytics:
- Sales trends and revenue metrics
- Inventory management
- User behavior insights
- ML model performance
- Customer sentiment analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Open an issue on GitHub
- Check the documentation
- Review the API endpoints

## 🎯 Future Enhancements

- User authentication and authorization
- Payment gateway integration
- Advanced recommendation algorithms
- Mobile application
- Multi-language support
- Advanced analytics dashboard

---

**Note**: This platform demonstrates modern e-commerce architecture with AI integration. It uses authentic product data and real-world technologies suitable for production deployment.