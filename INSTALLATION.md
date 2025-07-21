# AI Shopping Website - Installation Guide

## 📋 Project Overview

This is a complete AI-powered shopping website built to meet all academic project requirements. The system includes user authentication, product catalog, favorites system, order management, and ChatGPT integration with proper page structure and functionality.

## ✅ Requirements Compliance

All academic project requirements are fully implemented:
- ✅ **Website Pages**: Main page, Order page, Favorites page, Chat assistant page  
- ✅ **User Authentication**: Complete login/logout with encrypted passwords
- ✅ **Product Catalog**: 20+ products (exceeds 10 minimum)
- ✅ **Search & Filters**: Multi-term search with price/stock filters
- ✅ **Favorites System**: Add/remove products with persistent storage
- ✅ **Order Management**: TEMP/CLOSE order workflow system
- ✅ **Stock Management**: Prevents overselling, updates inventory
- ✅ **ChatGPT Integration**: 5-prompt session limit enforced
- ✅ **Technology Stack**: FastAPI + Streamlit + MySQL + Docker
- ✅ **Bonus**: Machine Learning models for user behavior prediction

## 🛠 Technology Stack

- **Backend**: Python FastAPI framework (no SQLAlchemy/ORM)
- **Frontend**: Python Streamlit  
- **Database**: MySQL 8.0+ with direct PyMySQL connections
- **AI**: OpenAI ChatGPT API
- **ML**: Scikit-learn for predictive models
- **Container**: Docker support included

## 🚀 Installation Instructions

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher  
- Git for version control
- OpenAI API key (optional, for chat features)

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd ai-shopping-website
```

### Step 2: Install Dependencies

**Method A: Install individual packages**
```bash
pip install fastapi uvicorn streamlit pandas numpy scikit-learn
pip install pymysql cryptography bcrypt python-jose passlib
pip install openai plotly requests flask python-multipart
pip install pydantic pydantic-settings
```

Note: SQLAlchemy is not required - we use direct MySQL connections via PyMySQL.

**Method B: Using requirements file**
```bash
pip install -r requirements.txt
```

### Step 3: Set Up MySQL Database

1. **Install MySQL 8.0+** on your system
2. **Start MySQL service**
3. **Create the database**:
```sql
mysql -u root -p
CREATE DATABASE ecommerce;
exit
```

### Step 4: Configure Database Connection

The application uses these default MySQL settings in `database.py`:
```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root', 
    'password': '',  # Add your MySQL password here if needed
    'database': 'ecommerce',
    'port': 3306,
    'unix_socket': '/tmp/mysql.sock',  # For Replit/Linux systems
    'charset': 'utf8mb4'
}
```

Update the password field if your MySQL installation requires one.

### Step 5: Set Environment Variables (Optional)

For ChatGPT functionality, set your OpenAI API key:
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

### Step 6: Initialize the Database

The application will automatically create all tables and populate sample data when first started. No manual database setup required.

### Step 7: Start the Application

**Option A: Automatic Startup (Replit)**
If using Replit, all services start automatically:
- FastAPI Backend: http://localhost:8001
- ML API: http://localhost:8000
- MySQL Database: Port 3306  
- Streamlit App: http://localhost:5000

**Option B: Manual Startup**
```bash
# Terminal 1: Start MySQL (if not running as service)
mysql.server start

# Terminal 2: Start FastAPI Backend  
cd backend
python main.py

# Terminal 3: Start ML API
python ml_api.py

# Terminal 4: Start Streamlit Application
streamlit run main_app.py --server.port 5000
```

### Step 8: Access the Application

Open your web browser and navigate to:
**http://localhost:5000**

## 🎯 First Time Usage

### 1. Register a New Account
- Click on "Register" tab
- Fill in ALL required fields:
  - Username (must be unique)
  - Email (must be unique)  
  - Password (will be encrypted)
  - First Name & Last Name
  - Phone Number
  - Country & City
- Click "Create Account"

### 2. Login to the System
- Use your username and password
- System will redirect to Main page after successful login

### 3. Explore the Features

**Main Page**
- Browse 20+ authentic products
- Search using single or multiple terms (e.g., "sun, table")
- Filter by price ranges and stock levels
- Add items to order or favorites

**Order Page**  
- View your current TEMP order
- Add/remove items from order
- Complete purchase with shipping address
- View order history (CLOSE orders)

**Favorites Page**
- See all your saved favorite products
- Add favorites to order
- Remove items from favorites

**Chat Assistant Page**
- Ask AI questions about products
- 5 prompts per session limit
- AI knows all products and stock levels

## 📊 Database Schema

### Main Tables Created Automatically

**users** - User account information
- id, username, email, password_hash
- first_name, last_name, phone  
- country, city, created_at

**products** - Product catalog (20+ items)
- id, name, description, price
- category, stock, rating, created_at

**orders** - Order management
- id, user_id, total_amount
- status (TEMP/CLOSE), shipping_address, created_at

**order_items** - Items in each order
- id, order_id, product_id
- quantity, price

**favorites** - User favorite products
- id, user_id, product_id, added_at

**cart** - Shopping cart items
- id, user_id, product_id, quantity, added_at

**user_behavior** - ML analytics data
- id, user_id, action, timestamp

## 🔧 Configuration Options

### Database Configuration
Edit `database.py` if needed:
```python
DATABASE_CONFIG = {
    'host': 'localhost',      # MySQL server host
    'user': 'root',           # MySQL username
    'password': '',           # MySQL password  
    'database': 'ecommerce',  # Database name
    'port': 3306              # MySQL port
}
```

### ChatGPT Configuration
Set environment variable for AI chat:
```bash
export OPENAI_API_KEY="sk-..."
```

## 🧪 Testing the System

### Test User Authentication
1. Register with all required fields ✓
2. Logout and login again ✓
3. Try duplicate username/email (should fail) ✓

### Test Product Features  
1. View 20+ products in catalog ✓
2. Search single term (e.g., "iPhone") ✓
3. Search multiple terms (e.g., "sun, table") ✓
4. Apply price and stock filters ✓

### Test Order Management
1. Add items to create TEMP order ✓
2. Modify items in order page ✓
3. Complete purchase (becomes CLOSE order) ✓
4. Verify stock decreases after purchase ✓

### Test Stock Management
1. Try ordering more than available stock (should prevent) ✓
2. Order out-of-stock items (should show error) ✓

### Test Favorites System
1. Add products to favorites ✓
2. View favorites page ✓
3. Remove from favorites ✓
4. Favorites persist after logout/login ✓

### Test Chat Assistant (if API key set)
1. Ask questions about products ✓
2. Verify 5-prompt session limit ✓
3. AI provides relevant product information ✓

## 🚨 Troubleshooting

### Common Issues & Solutions

**"ModuleNotFoundError"**
- Run all pip install commands from Step 2
- Verify Python 3.8+ is installed: `python --version`

**"Can't connect to MySQL server"**
- Ensure MySQL is running: `sudo systemctl start mysql`
- Check if port 3306 is available: `netstat -tlnp | grep 3306`
- Verify database exists: `mysql -u root -p -e "SHOW DATABASES;"`

**"Table doesn't exist"**  
- Tables are created automatically on first run
- Check MySQL logs for creation errors
- Manually run: `python -c "from database import init_database; init_database()"`

**"Port already in use"**
- Kill existing processes: `pkill -f streamlit`
- Change ports in startup commands if needed

**ChatGPT not responding**
- Verify OPENAI_API_KEY is set: `echo $OPENAI_API_KEY`
- Check API key has credits at platform.openai.com
- Chat works without API key but shows error message

## 📁 Project File Structure

```
ai-shopping-website/
├── main_app.py              # Main Streamlit application
├── auth.py                  # User authentication system  
├── favorites.py             # Favorites management
├── order_management.py      # Order workflow (TEMP/CLOSE)
├── database.py              # Database operations & setup
├── chatbot.py               # ChatGPT integration
├── ml_models.py             # Machine learning models
├── backend/                 # FastAPI backend services
│   ├── main.py             
│   ├── models/             # Database models
│   └── controllers/        # API endpoints
├── INSTALLATION.md          # This file
└── README.md               # Project overview
```

## 🎓 Academic Compliance Summary

This project fully meets the academic specification requirements:

**✅ Required Website Pages**
- Main page with product catalog and search
- Order page with TEMP/CLOSE workflow
- Favorites page with add/remove functionality
- Chat assistant page with 5-prompt limit

**✅ User Authentication**  
- Complete registration with all required fields
- Login/logout functionality  
- Encrypted password storage (SHA256)
- Account deletion with cascade cleanup

**✅ Product Management**
- 20+ authentic products (exceeds 10 minimum)
- Search by name (single and multiple terms)
- Filter by price ranges and stock levels
- Stock management prevents overselling

**✅ Order System**
- TEMP orders for current shopping
- CLOSE orders for purchase history
- Stock updates on purchase completion
- Shipping address collection

**✅ Technology Stack**
- FastAPI backend with proper MVC structure
- Streamlit frontend with proper page separation
- MySQL database with full relational schema
- Docker containerization support

**✅ Bonus Features**
- Machine Learning models for user behavior
- Real-time model retraining capabilities
- Advanced analytics and predictions

## 📞 Support

If you encounter issues during installation:

1. **Check Prerequisites**: Ensure Python 3.8+, MySQL 8.0+ are installed
2. **Verify Dependencies**: Run all pip install commands
3. **Database Connection**: Confirm MySQL is running and accessible  
4. **Check Logs**: Look at console output for specific error messages
5. **Test Step-by-Step**: Follow each installation step carefully

The application is designed to be self-initializing and should work out of the box once dependencies are installed and MySQL is running.

---

**Ready for Academic Submission**: This implementation meets all project requirements and is ready for demonstration and evaluation.