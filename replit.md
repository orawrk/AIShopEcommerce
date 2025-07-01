# AI-Powered E-Commerce Platform

## Overview

This is a comprehensive AI-powered e-commerce platform that combines modern web technologies with machine learning capabilities. The system features a FastAPI backend, Streamlit frontend, and integrated AI services including ChatGPT customer support and real-time ML model retraining.

## System Architecture

The application follows a microservices architecture with clear separation of concerns:

### Frontend Layer
- **Streamlit Application** (port 5000): Interactive web interface for customers and admins
- **Real-time Dashboard**: ML model monitoring and retraining controls
- **Customer Support Interface**: ChatGPT-powered chatbot integration

### Backend Layer
- **FastAPI REST API** (port 8001): Main business logic and data operations
- **ML API Service** (port 8000): Machine learning predictions and model management
- **PostgreSQL Database**: Product catalog, user data, orders, and behavior tracking

### AI/ML Layer
- **OpenAI GPT Integration**: Customer support chatbot
- **Scikit-learn Models**: User behavior prediction (churn, spending)
- **Real-time Model Retraining**: Automated ML pipeline with performance monitoring

## Key Components

### Database Models
- **Products**: Authentic product catalog with 18+ items across 5 categories
- **Users**: Customer authentication and profile management
- **Orders & Cart**: E-commerce transaction handling
- **User Behavior**: ML analytics data collection

### API Controllers
- **Product Controller**: CRUD operations, search, and inventory management
- **User Controller**: Authentication, registration, and profile management
- **Order Controller**: Order processing and status tracking
- **Cart Controller**: Shopping cart operations

### AI Services
- **ChatGPT Integration**: Customer support with context-aware responses
- **ML Models**: Predictive analytics for user behavior
- **Real-time Retraining**: Automated model updates based on new data

### Business Services
- **Product Service**: Business logic for product operations
- **User Service**: Authentication and user management
- **Order Service**: Order processing and fulfillment
- **Cart Service**: Shopping cart management

## Data Flow

1. **Customer Interaction**: Users interact through Streamlit frontend
2. **API Communication**: Frontend communicates with FastAPI backend via REST APIs
3. **Data Processing**: Business services handle validation and processing
4. **Database Operations**: SQLAlchemy ORM manages data persistence
5. **ML Integration**: User actions trigger behavior tracking for ML models
6. **AI Response**: ChatGPT provides intelligent customer support
7. **Analytics**: ML API provides predictive insights and automated retraining

## External Dependencies

### Core Technologies
- **FastAPI**: Modern Python web framework for REST APIs
- **Streamlit**: Python-based web application framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Development database (MySQL-compatible design)

### AI/ML Stack
- **OpenAI API**: GPT-4o model for customer support
- **Scikit-learn**: Machine learning models and algorithms
- **Pandas/NumPy**: Data processing and analysis
- **Plotly**: Interactive data visualizations

### Development Tools
- **Docker**: Containerization support
- **Uvicorn**: ASGI server for FastAPI
- **Pydantic**: Data validation and serialization

## Deployment Strategy

### Local Development
- SQLite database for easy setup
- Environment variables for configuration
- Docker Compose for multi-service orchestration

### Production Considerations
- MySQL/PostgreSQL database migration support
- Environment-based configuration management
- Containerized deployment ready
- Health check endpoints for monitoring

### Key Configuration
- Database: PostgreSQL (production-ready)
- API Ports: FastAPI (8001), ML API (8000), Streamlit (5000)
- External APIs: OpenAI GPT-4o integration
- Authentication: JWT tokens with bcrypt password hashing

## Changelog

- July 01, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.