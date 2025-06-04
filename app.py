import streamlit as st
import pandas as pd
import sqlite3
import json
import requests
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from database import init_database, get_products, add_to_cart, get_cart_items, create_order, get_user_orders, update_inventory
from chatbot import get_chatbot_response
from ml_models import load_user_behavior_model, predict_user_behavior
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database on startup
init_database()

# Page configuration
st.set_page_config(
    page_title="AI E-Commerce Platform",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = 1  # Default user for demo
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Products"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def main():
    st.title("🛒 AI-Powered E-Commerce Platform")
    
    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox(
            "Select Page",
            ["Products", "Shopping Cart", "Orders", "AI Chat Support", "User Analytics", "Admin Dashboard"]
        )
        st.session_state.current_page = page
        
        # User info section
        st.header("User Info")
        st.write(f"User ID: {st.session_state.user_id}")
        
        # Cart summary
        cart_items = get_cart_items(st.session_state.user_id)
        total_items = sum([item[3] for item in cart_items])
        st.write(f"Cart Items: {total_items}")
    
    # Main content based on selected page
    if st.session_state.current_page == "Products":
        show_products_page()
    elif st.session_state.current_page == "Shopping Cart":
        show_cart_page()
    elif st.session_state.current_page == "Orders":
        show_orders_page()
    elif st.session_state.current_page == "AI Chat Support":
        show_chat_page()
    elif st.session_state.current_page == "User Analytics":
        show_analytics_page()
    elif st.session_state.current_page == "Admin Dashboard":
        show_admin_dashboard()

def show_products_page():
    st.header("Product Catalog")
    
    # Search and filter functionality
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("Search products", placeholder="Enter product name or description")
    
    with col2:
        categories = ["All", "Electronics", "Clothing", "Books", "Home & Garden", "Sports"]
        selected_category = st.selectbox("Category", categories)
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Name", "Price (Low to High)", "Price (High to Low)", "Rating"])
    
    # Get products from database
    try:
        products = get_products(search_term, selected_category if selected_category != "All" else None, sort_by)
        
        if not products:
            st.warning("No products found matching your criteria.")
            return
        
        # Display products in a grid
        cols_per_row = 3
        for i in range(0, len(products), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(products):
                    product = products[i + j]
                    with col:
                        display_product_card(product)
        
        # AI-powered recommendations
        st.header("🤖 AI Recommendations for You")
        recommendations = get_ai_recommendations(st.session_state.user_id)
        
        if recommendations:
            rec_cols = st.columns(min(len(recommendations), 3))
            for idx, rec in enumerate(recommendations[:3]):
                with rec_cols[idx]:
                    display_product_card(rec)
        else:
            st.info("Browse more products to get personalized recommendations!")
            
    except Exception as e:
        logger.error(f"Error loading products: {e}")
        st.error("Failed to load products. Please try again later.")

def display_product_card(product):
    """Display a product card with details and add to cart button"""
    product_id, name, description, price, category, stock, rating = product
    
    st.subheader(name)
    st.write(f"**Category:** {category}")
    st.write(f"**Price:** ${price:.2f}")
    st.write(f"**Rating:** {'⭐' * int(rating)} ({rating}/5)")
    st.write(f"**Stock:** {stock} available")
    
    if len(description) > 100:
        with st.expander("Product Description"):
            st.write(description)
    else:
        st.write(description)
    
    # Add to cart functionality
    col1, col2 = st.columns(2)
    with col1:
        quantity = st.number_input(f"Quantity", min_value=1, max_value=stock, value=1, key=f"qty_{product_id}")
    
    with col2:
        if st.button(f"Add to Cart", key=f"add_{product_id}"):
            if stock >= quantity:
                success = add_to_cart(st.session_state.user_id, product_id, quantity)
                if success:
                    st.success(f"Added {quantity} {name}(s) to cart!")
                    st.rerun()
                else:
                    st.error("Failed to add item to cart.")
            else:
                st.error("Not enough stock available.")

def show_cart_page():
    st.header("🛒 Shopping Cart")
    
    cart_items = get_cart_items(st.session_state.user_id)
    
    if not cart_items:
        st.info("Your cart is empty. Start shopping to add items!")
        return
    
    # Display cart items
    total_amount = 0
    for item in cart_items:
        cart_id, product_name, price, quantity, product_id = item
        item_total = price * quantity
        total_amount += item_total
        
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
        
        with col1:
            st.write(f"**{product_name}**")
        with col2:
            st.write(f"${price:.2f}")
        with col3:
            # Quantity update
            new_qty = st.number_input("Qty", min_value=1, value=quantity, key=f"cart_qty_{cart_id}")
            if new_qty != quantity:
                # Update cart quantity logic would go here
                pass
        with col4:
            st.write(f"${item_total:.2f}")
        with col5:
            if st.button("Remove", key=f"remove_{cart_id}"):
                # Remove item logic would go here
                st.rerun()
    
    st.divider()
    
    # Cart summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Total: ${total_amount:.2f}")
    
    with col2:
        if st.button("Proceed to Checkout", type="primary"):
            # Create order
            order_id = create_order(st.session_state.user_id, cart_items, total_amount)
            if order_id:
                st.success(f"Order #{order_id} placed successfully!")
                # Clear cart logic would go here
                st.rerun()
            else:
                st.error("Failed to place order. Please try again.")

def show_orders_page():
    st.header("📦 Order History")
    
    orders = get_user_orders(st.session_state.user_id)
    
    if not orders:
        st.info("No orders found.")
        return
    
    for order in orders:
        order_id, order_date, total_amount, status = order
        
        with st.expander(f"Order #{order_id} - {order_date} - ${total_amount:.2f}"):
            st.write(f"**Status:** {status}")
            st.write(f"**Date:** {order_date}")
            st.write(f"**Total:** ${total_amount:.2f}")
            
            # Order tracking simulation
            if status == "Processing":
                st.progress(0.3)
                st.write("📦 Order is being prepared")
            elif status == "Shipped":
                st.progress(0.7)
                st.write("🚚 Order is on the way")
            elif status == "Delivered":
                st.progress(1.0)
                st.write("✅ Order delivered")

def show_chat_page():
    st.header("🤖 AI Customer Support")
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.write(f"**You:** {message['content']}")
            else:
                st.write(f"**AI Assistant:** {message['content']}")
    
    # Chat input
    user_input = st.text_input("Type your message here...", key="chat_input")
    
    if st.button("Send") and user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        try:
            # Get AI response
            ai_response = get_chatbot_response(user_input, st.session_state.user_id)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
        except Exception as e:
            logger.error(f"Chatbot error: {e}")
            st.error("Sorry, I'm having trouble responding right now. Please try again later.")
    
    # Quick action buttons
    st.subheader("Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Track My Order"):
            st.session_state.chat_history.append({"role": "user", "content": "I want to track my order"})
            ai_response = get_chatbot_response("I want to track my order", st.session_state.user_id)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
    
    with col2:
        if st.button("Return Policy"):
            st.session_state.chat_history.append({"role": "user", "content": "What is your return policy?"})
            ai_response = get_chatbot_response("What is your return policy?", st.session_state.user_id)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
    
    with col3:
        if st.button("Product Recommendations"):
            st.session_state.chat_history.append({"role": "user", "content": "Can you recommend products for me?"})
            ai_response = get_chatbot_response("Can you recommend products for me?", st.session_state.user_id)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()

def show_analytics_page():
    st.header("📊 User Behavior Analytics")
    
    try:
        # Call ML API for user behavior prediction
        ml_api_url = "http://localhost:8000/predict"  # Flask API endpoint
        
        # Get user behavior prediction
        response = requests.post(
            ml_api_url,
            json={"user_id": st.session_state.user_id},
            timeout=10
        )
        
        if response.status_code == 200:
            predictions = response.json()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎯 Churn Prediction")
                churn_prob = predictions.get("churn_probability", 0)
                
                # Create gauge chart for churn probability
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = churn_prob * 100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Churn Risk (%)"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "red" if churn_prob > 0.7 else "orange" if churn_prob > 0.4 else "green"},
                        'steps': [
                            {'range': [0, 40], 'color': "lightgreen"},
                            {'range': [40, 70], 'color': "yellow"},
                            {'range': [70, 100], 'color': "lightcoral"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 70
                        }
                    }
                ))
                st.plotly_chart(fig_gauge, use_container_width=True)
                
                if churn_prob > 0.7:
                    st.error("⚠️ High churn risk! Consider offering special promotions.")
                elif churn_prob > 0.4:
                    st.warning("⚡ Moderate churn risk. Monitor user engagement.")
                else:
                    st.success("✅ Low churn risk. User is likely to stay.")
            
            with col2:
                st.subheader("💰 Spending Prediction")
                spending_pred = predictions.get("predicted_spending", 0)
                
                st.metric("Predicted Monthly Spending", f"${spending_pred:.2f}")
                
                # Spending category
                if spending_pred > 500:
                    st.success("🔥 High-value customer")
                elif spending_pred > 200:
                    st.info("📈 Regular customer")
                else:
                    st.warning("💡 Potential for growth")
        
        else:
            st.error("Failed to get ML predictions. Please ensure the ML API is running.")
            
    except requests.exceptions.RequestException as e:
        logger.error(f"ML API connection error: {e}")
        st.error("ML API is not available. Please start the ML service.")
    except Exception as e:
        logger.error(f"Analytics error: {e}")
        st.error("Failed to load analytics data.")
    
    # User activity visualization
    st.subheader("📈 User Activity Trends")
    
    # Generate sample activity data for visualization
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    activity_data = pd.DataFrame({
        'date': dates,
        'orders': [max(0, int(pd.np.random.normal(2, 1))) for _ in dates],
        'page_views': [max(0, int(pd.np.random.normal(15, 5))) for _ in dates],
        'time_spent': [max(0, pd.np.random.normal(25, 10)) for _ in dates]
    })
    
    # Activity charts
    tab1, tab2, tab3 = st.tabs(["Orders", "Page Views", "Time Spent"])
    
    with tab1:
        fig_orders = px.line(activity_data, x='date', y='orders', title='Daily Orders')
        st.plotly_chart(fig_orders, use_container_width=True)
    
    with tab2:
        fig_views = px.line(activity_data, x='date', y='page_views', title='Daily Page Views')
        st.plotly_chart(fig_views, use_container_width=True)
    
    with tab3:
        fig_time = px.line(activity_data, x='date', y='time_spent', title='Daily Time Spent (minutes)')
        st.plotly_chart(fig_time, use_container_width=True)

def show_admin_dashboard():
    st.header("⚙️ Admin Dashboard")
    
    # Admin functionality
    tab1, tab2, tab3 = st.tabs(["Inventory Management", "Order Management", "User Analytics"])
    
    with tab1:
        st.subheader("📦 Inventory Management")
        
        # Get all products for inventory management
        products = get_products()
        
        if products:
            df = pd.DataFrame(products, columns=['ID', 'Name', 'Description', 'Price', 'Category', 'Stock', 'Rating'])
            
            # Display products table
            st.dataframe(df, use_container_width=True)
            
            # Update inventory form
            st.subheader("Update Inventory")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                product_names = [p[1] for p in products]
                selected_product = st.selectbox("Select Product", product_names)
            
            with col2:
                new_stock = st.number_input("New Stock Quantity", min_value=0, value=0)
            
            with col3:
                if st.button("Update Stock"):
                    product_id = next(p[0] for p in products if p[1] == selected_product)
                    success = update_inventory(product_id, new_stock)
                    if success:
                        st.success("Inventory updated successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to update inventory.")
    
    with tab2:
        st.subheader("📋 Order Management")
        st.info("Order management functionality would be implemented here.")
        
        # Sample order statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Orders", "1,234")
        with col2:
            st.metric("Pending Orders", "56")
        with col3:
            st.metric("Revenue Today", "$2,456")
        with col4:
            st.metric("Revenue This Month", "$45,678")
    
    with tab3:
        st.subheader("👥 User Analytics Overview")
        st.info("Comprehensive user analytics would be displayed here.")
        
        # Sample user metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Users", "5,678")
        with col2:
            st.metric("Active Users", "1,234")
        with col3:
            st.metric("Churn Rate", "12%")

def get_ai_recommendations(user_id):
    """Get AI-powered product recommendations"""
    try:
        products = get_products()
        if len(products) < 3:
            return products
        
        # Simple recommendation based on user behavior
        # In a real implementation, this would use collaborative filtering or content-based filtering
        import random
        return random.sample(products, min(3, len(products)))
        
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        return []

if __name__ == "__main__":
    main()
