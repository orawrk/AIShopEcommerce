# Deployment Guide - AI E-Commerce Platform

This guide provides comprehensive instructions for deploying the AI-powered e-commerce platform in various environments.

> 📖 **Visual Reference**: See [VISUAL_GUIDE.md](VISUAL_GUIDE.md) for screenshots and visual walkthroughs of all platform features.

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Docker & Docker Compose (optional)
- OpenAI API Key
- Git

## Environment Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd ai-ecommerce-platform
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Configuration
```bash
# PostgreSQL setup
createdb ecommerce
export DATABASE_URL="postgresql://username:password@localhost:5432/ecommerce"
```

### 4. Environment Variables
Create `.env` file:
```bash
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce
PGHOST=localhost
PGPORT=5432
PGDATABASE=ecommerce
PGUSER=username
PGPASSWORD=password

# OpenAI API
OPENAI_API_KEY=your-openai-api-key

# Application
DEBUG=True
SECRET_KEY=your-secret-key-here
```

### 5. Initialize Database
```bash
cd backend
python seed_data.py
```

## Deployment Options

### Option 1: Local Development

Start each service in separate terminals:

```bash
# Terminal 1 - FastAPI Backend
cd backend
python main.py
# Runs on: http://localhost:8001

# Terminal 2 - ML API
python ml_api.py
# Runs on: http://localhost:8000

# Terminal 3 - Streamlit Frontend
streamlit run app.py --server.port 5000
# Runs on: http://localhost:5000
```

### Option 2: Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 3: Production Deployment

#### Using Docker with Production Configuration

1. **Create production environment file:**
```bash
cp .env.example .env.production
# Edit with production values
```

2. **Build production images:**
```bash
docker-compose -f docker-compose.prod.yml build
```

3. **Deploy with orchestration:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

#### Using Systemd Services

1. **Create service files:**
```bash
# /etc/systemd/system/ecommerce-backend.service
[Unit]
Description=E-Commerce FastAPI Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/project/backend
Environment=DATABASE_URL=postgresql://...
ExecStart=/path/to/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

2. **Enable and start services:**
```bash
sudo systemctl enable ecommerce-backend
sudo systemctl start ecommerce-backend
```

## Service Configuration

### FastAPI Backend (Port 8001)
- **Purpose**: RESTful API for product management
- **Dependencies**: PostgreSQL, Python 3.11+
- **Health Check**: `GET /health`
- **Documentation**: `http://localhost:8001/docs`

### ML API (Port 8000)
- **Purpose**: Machine learning predictions
- **Dependencies**: Scikit-learn, trained models
- **Health Check**: `GET /health`
- **Endpoints**: `/predict`, `/retrain`, `/model-info`

### Streamlit Frontend (Port 5000)
- **Purpose**: User interface and admin dashboard
- **Dependencies**: Backend APIs, database
- **Features**: Product catalog, cart, orders, analytics

## Database Management

### Initial Setup
```sql
-- Create database
CREATE DATABASE ecommerce;

-- Create user
CREATE USER ecommerce_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE ecommerce TO ecommerce_user;
```

### Data Seeding
```bash
# Populate with authentic product data
python backend/seed_data.py
```

### Backup & Restore
```bash
# Backup
pg_dump ecommerce > backup.sql

# Restore
psql ecommerce < backup.sql
```

## Monitoring & Logging

### Application Logs
```bash
# View real-time logs
tail -f logs/application.log

# Docker logs
docker-compose logs -f [service-name]
```

### Health Monitoring
```bash
# Check service health
curl http://localhost:8001/health
curl http://localhost:8000/health
curl http://localhost:5000
```

### Performance Monitoring
- Monitor database connections
- Track API response times
- Monitor memory usage
- Check ML model performance

## Security Considerations

### API Security
- Use HTTPS in production
- Implement rate limiting
- Validate all inputs
- Use environment variables for secrets

### Database Security
- Use strong passwords
- Limit database access
- Regular security updates
- Backup encryption

### Application Security
- Keep dependencies updated
- Monitor for vulnerabilities
- Implement proper authentication
- Secure API endpoints

## Scaling Considerations

### Horizontal Scaling
- Load balance FastAPI instances
- Database read replicas
- Container orchestration with Kubernetes

### Performance Optimization
- Database indexing
- Caching strategies
- CDN for static assets
- ML model optimization

## Troubleshooting

### Common Issues

**Database Connection Failed**
```bash
# Check connection
psql -h localhost -U username -d ecommerce

# Verify environment variables
echo $DATABASE_URL
```

**FastAPI Not Starting**
```bash
# Check Python dependencies
pip install -r requirements.txt

# Verify database is running
systemctl status postgresql
```

**ML Models Not Loading**
```bash
# Check model files exist
ls -la models/

# Verify scikit-learn version
pip show scikit-learn
```

**Streamlit Connection Error**
```bash
# Check backend services
curl http://localhost:8001/health
curl http://localhost:8000/health

# Verify port availability
netstat -tulpn | grep :5000
```

## API Documentation

### FastAPI Swagger UI
- URL: `http://localhost:8001/docs`
- Interactive API documentation
- Test endpoints directly

### ML API Endpoints
```bash
# Health check
GET /health

# User prediction
POST /predict
{
  "user_id": 123
}

# Model retraining
POST /retrain

# Model information
GET /model-info
```

## Support

For deployment issues:
1. Check logs for error messages
2. Verify all environment variables
3. Test database connectivity
4. Confirm all services are running
5. Review this deployment guide

## Updates & Maintenance

### Regular Maintenance
- Update dependencies monthly
- Retrain ML models weekly
- Database maintenance quarterly
- Security patches as needed

### Deployment Updates
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Restart services
docker-compose restart
```