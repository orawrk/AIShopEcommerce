# Screenshot Capture Guide
## AI Shopping Platform Documentation

### Quick Setup for Screenshots

1. **Ensure Services are Running**:
   ```bash
   # Check if all services are active
   curl http://localhost:5000  # Streamlit App
   curl http://localhost:8001/docs  # FastAPI Backend
   curl http://localhost:8000/health  # ML API
   ```

2. **Browser Setup**:
   - Use Chrome or Firefox for best results
   - Set browser window to 1920x1080 for consistent screenshots
   - Disable browser extensions that might interfere

3. **Application Access**:
   - Main URL: http://localhost:5000
   - API Documentation: http://localhost:8001/docs
   - ML API Health: http://localhost:8000/health

### Screenshot Checklist

#### 📋 Required Screenshots

- [ ] **01_login_page.png** - Authentication interface
- [ ] **02_product_catalog.png** - Main product browsing
- [ ] **03_search_filter.png** - Search and filtering demo
- [ ] **04_shopping_cart.png** - Cart management interface
- [ ] **05_order_history.png** - Order tracking and history
- [ ] **06_favorites.png** - Wishlist/favorites feature
- [ ] **07_ai_chat.png** - ChatGPT integration demo
- [ ] **08_user_profile.png** - User account management
- [ ] **09_navigation.png** - App navigation and menu
- [ ] **10_product_details.png** - Individual product view

#### 🎯 Capture Tips

1. **Clean Interface**: Clear any debug messages or errors before capturing
2. **Sample Data**: Ensure products are loaded and visible
3. **User Flow**: Capture logical user journey steps
4. **Feature Highlights**: Focus on key functionality
5. **Consistent Styling**: Maintain same zoom level and window size

### Test User Account
For demonstration purposes, you can create a test account:
- Username: demo_user
- Email: demo@example.com
- Password: demo123
- Name: Demo User

### Step-by-Step Capture Process

#### Step 1: Login/Registration Page
1. Navigate to http://localhost:5000
2. Capture the login/registration interface
3. Show both login and register tabs

#### Step 2: Product Catalog
1. Login with test account
2. Capture main product catalog view
3. Ensure products are displayed in grid format

#### Step 3: Search & Filter
1. Use search box to search for "phone" or "laptop"
2. Demonstrate price filtering
3. Show category selection

#### Step 4: Shopping Cart
1. Add 2-3 products to cart
2. Navigate to cart/orders page
3. Show item management (quantities, removal)

#### Step 5: Order Management
1. Complete an order if possible
2. Show order history
3. Display order details

#### Step 6: Favorites
1. Add products to favorites
2. Navigate to favorites page
3. Show favorite management

#### Step 7: AI Chat
1. Navigate to AI Chat section
2. Send a message like "Help me find a good laptop"
3. Capture the conversation interface

### Image Specifications
- **Format**: PNG (preferred) or JPG
- **Resolution**: 1920x1080 or similar 16:9 ratio
- **Quality**: High quality, clear text
- **File Size**: < 2MB per image
- **Naming**: Use descriptive filenames with numbers

### Troubleshooting

#### Common Issues:
1. **No Products Showing**: Check database connection and run database setup
2. **Login Issues**: Verify user creation process
3. **Services Not Running**: Restart workflows in proper order
4. **Slow Loading**: Wait for all services to fully initialize

#### Service Restart Order:
1. MySQL Database
2. FastAPI Backend  
3. ML API
4. Streamlit App

### Manual Screenshot Alternative

If automated capture fails, use these manual steps:

1. **Browser Screenshots**:
   - Press F11 for fullscreen (optional)
   - Use browser's built-in screenshot tools
   - Or use system screenshot tools (Cmd+Shift+4 on Mac, PrtScn on Windows)

2. **Screen Recording**:
   - Record a demo video showing all features
   - Extract key frames as screenshots
   - Use tools like OBS Studio or QuickTime

3. **Mobile Screenshots**:
   - Test on mobile devices
   - Capture responsive design
   - Show touch interactions

### Documentation Integration

After capturing screenshots:

1. **File Organization**:
   ```
   docs/images/
   ├── screenshots/
   │   ├── 01_login_page.png
   │   ├── 02_product_catalog.png
   │   └── ...
   └── README.md
   ```

2. **Update Presentation**:
   - Replace placeholder text with actual image references
   - Add captions and descriptions
   - Include in project documentation

3. **Create Visual Guide**:
   - Combine screenshots into a visual user guide
   - Add annotations and callouts
   - Export as PDF for easy sharing

This guide ensures comprehensive visual documentation of the AI Shopping Platform for presentations and demonstrations.