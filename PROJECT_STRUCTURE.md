# Project Structure - AI E-Commerce Platform

This document outlines the complete file structure and architecture of the AI-powered e-commerce platform.

## Repository Overview

```
ai-ecommerce-platform/
├── README.md                    # Main project documentation
├── LICENSE                      # MIT License
├── DEPLOYMENT.md               # Deployment guide
├── PROJECT_STRUCTURE.md        # This file
├── .gitignore                  # Git ignore patterns
├── pyproject.toml              # Python dependencies
├── uv.lock                     # Dependency lock file
├── docker-compose.yml          # Docker services configuration
├── Dockerfile.backend          # Backend container definition
└── .streamlit/
    └── config.toml             # Streamlit configuration
```

## Backend Architecture (FastAPI)

```
backend/
├── __init__.py                 # Package initialization
├── main.py                     # FastAPI application entry point
├── seed_data.py               # Database seeding with authentic products
├── config/                    # Configuration management
│   ├── __init__.py
│   ├── database.py            # Database connection setup (no ORM)
│   └── settings.py            # Application settings and environment variables
├── models/                    # Database model definitions (no ORM)
│   ├── __init__.py
│   ├── base.py                # Base database operations
│   ├── product.py             # Product data structure and queries
│   ├── user.py                # User data structure and queries
│   ├── order.py               # Order and OrderItem queries
│   ├── cart.py                # Shopping cart operations
│   ├── user_behavior.py       # User behavior tracking for ML
│   └── enums.py               # Enumeration definitions
├── schemas/                   # Pydantic schemas for API validation
│   ├── __init__.py
│   ├── product_schemas.py     # Product request/response schemas
│   ├── user_schemas.py        # User authentication schemas
│   ├── order_schemas.py       # Order management schemas
│   └── cart_schemas.py        # Cart operation schemas
├── controllers/               # API route controllers
│   ├── __init__.py
│   ├── product_controller.py  # Product CRUD operations
│   ├── user_controller.py     # User authentication
│   ├── order_controller.py    # Order management
│   └── cart_controller.py     # Shopping cart operations
├── services/                  # Business logic layer
│   ├── __init__.py
│   ├── product_service.py     # Product business logic
│   ├── user_service.py        # User management
│   ├── order_service.py       # Order processing
│   └── cart_service.py        # Cart management
└── utils/                     # Utility functions
    └── __init__.py
```

## Frontend Application (Streamlit)

```
├── app.py                     # Main Streamlit application
├── database.py                # Database utilities and MySQL operations
├── utils.py                   # Helper functions and utilities
└── .streamlit/
    └── config.toml            # Streamlit server configuration
```

## AI/ML Components

```
├── chatbot.py                 # OpenAI GPT integration for customer support
├── ml_api.py                  # Flask API for machine learning services
├── ml_models.py               # ML model training and prediction logic
└── models/                    # Trained ML models directory
    ├── churn_model.pkl        # User churn prediction model
    ├── spending_model.pkl     # User spending prediction model
    └── scaler.pkl             # Feature scaling for ML models
```

## Data Management

```
├── data/                      # Data files and samples
│   ├── sample_products.csv    # Product catalog data
│   └── user_behavior_training.csv  # ML training data
└── mysql_data/               # MySQL database files (development)
```

## Key Features by Component

### FastAPI Backend (Port 8001)
- **Product Management**: Full CRUD operations with authentic product data
- **User Authentication**: JWT-based authentication system
- **Order Processing**: Complete order lifecycle management
- **Shopping Cart**: Real-time cart operations
- **Database Integration**: MySQL with direct PyMySQL connections
- **API Documentation**: Automatic Swagger/OpenAPI documentation

### ML API (Port 8000)
- **User Behavior Prediction**: Churn and spending pattern analysis
- **Model Training**: Automated retraining with latest data
- **Health Monitoring**: Model status and performance tracking
- **Flask Framework**: Lightweight API for ML operations

### Streamlit Frontend (Port 5000)
- **Product Catalog**: Browse authentic products across 5 categories
- **Shopping Experience**: Add to cart, checkout, order tracking
- **AI Chat Support**: Integrated ChatGPT customer service
- **Admin Dashboard**: Inventory management and analytics
- **Real-time Updates**: Live order status and inventory tracking

## Database Schema

### Core Tables
- **products**: Product catalog with authentic brand data
- **users**: User authentication and profiles
- **orders**: Order management and tracking
- **order_items**: Individual items within orders
- **cart_items**: Shopping cart contents
- **user_behaviors**: ML training data for predictions

### Authentic Product Data
The platform includes real products from major brands:
- **Electronics**: iPhone 15 Pro, MacBook Air M3, Sony WH-1000XM5
- **Clothing**: Levi's 501 Jeans, Nike Air Force 1, Patagonia Jacket
- **Books**: The Psychology of Money, Atomic Habits, Sapiens
- **Home & Garden**: Dyson V15 Vacuum, Instant Pot, Philips Hue
- **Sports**: Hydro Flask, Yeti Tumbler, Theraband Equipment

## Integration Points

### External APIs
- **OpenAI GPT**: Customer support chatbot with product context
- **MySQL**: Production database with authentic product data
- **FastAPI**: RESTful API backend with automatic documentation

### Internal Services
- **Database Layer**: Direct MySQL connections with PyMySQL
- **Business Logic**: Service layer pattern for clean architecture
- **ML Pipeline**: Scikit-learn models with automated training
- **Frontend**: Streamlit with real-time data integration

## Development Workflow

### Local Development
1. Start MySQL database
2. Run FastAPI backend (port 8001)
3. Start ML API service (port 8000)
4. Launch Streamlit frontend (port 5000)

### Docker Deployment
- Multi-container setup with Docker Compose
- Production-ready configuration
- Automated service orchestration

## Security Features

### Authentication
- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control

### Data Protection
- Environment variable configuration
- Database connection security
- API input validation

## Performance Optimization

### Backend
- Database indexing for fast queries
- Pagination for large datasets
- Efficient MySQL queries with PyMySQL

### Frontend
- Streamlit caching for improved performance
- Real-time updates without full page refresh
- Optimized image loading

### ML Components
- Pre-trained model caching
- Efficient feature processing
- Scalable prediction endpoints

## Monitoring & Analytics

### Application Metrics
- API response times
- Database query performance
- User behavior tracking
- ML model accuracy

### Business Intelligence
- Sales analytics dashboard
- Inventory management
- Customer behavior insights
- Predictive analytics

This structure provides a comprehensive, production-ready e-commerce platform with modern architecture patterns, authentic data integration, and advanced AI capabilities.