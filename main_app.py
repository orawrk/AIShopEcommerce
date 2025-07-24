"""
AI Shopping Website - Complete Implementation
Meeting all project requirements with proper page structure and authentication
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib

# Import custom modules
from database import get_products, get_connection
from auth import create_user, authenticate_user, get_user_by_id, delete_user_account, load_users_from_file_to_db
from favorites import add_to_favorites, remove_from_favorites, get_user_favorites, is_favorite
from order_management import (
    add_item_to_temp_order, get_temp_order, complete_order, 
    get_user_orders, get_order_items, remove_item_from_temp_order
)
from chatbot import get_chatbot_response

# Configure page
st.set_page_config(
    page_title="AI Shopping Website",
    page_icon="🛒",
    layout="wide"
)

# Load users from file to database on startup
if 'users_loaded' not in st.session_state:
    try:
        load_users_from_file_to_db()
        st.session_state.users_loaded = True
    except Exception as e:
        st.session_state.users_loaded = False

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_info' not in st.session_state:
    st.session_state.user_info = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Main"
if 'chat_prompts_count' not in st.session_state:
    st.session_state.chat_prompts_count = 0
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def login_page():
    """User authentication page"""
    st.title("🔐 Login / Register")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if username and password:
                    user = authenticate_user(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user['id']
                        st.session_state.user_info = user
                        st.session_state.chat_prompts_count = 0  # Reset chat prompts
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please fill in all fields")
    
    with tab2:
        st.subheader("Create New Account")
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name*")
                last_name = st.text_input("Last Name*")
                username = st.text_input("Username*")
                email = st.text_input("Email*")
            with col2:
                phone = st.text_input("Phone*")
                country = st.text_input("Country*")
                city = st.text_input("City*")
                password = st.text_input("Password*", type="password")
            
            # Center the Create Account button
            st.markdown("<br>", unsafe_allow_html=True)
            col_left, col_center, col_right = st.columns([1, 2, 1])
            with col_center:
                submit = st.form_submit_button("Create Account", use_container_width=True)
            
            if submit:
                if all([username, email, password, first_name, last_name, phone, country, city]):
                    success, message = create_user(username, email, password, first_name, last_name, phone, country, city)
                    if success:
                        st.success(message)
                        st.info("You can now login with your credentials")
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all required fields")

def main_page():
    """Main page with product catalog and search - accessible to all users"""
    st.title("🛒 AI Shopping Website")
    st.markdown("### Welcome to our AI-powered shopping platform!")
    
    # Show login prompt for guest users
    if not st.session_state.logged_in:
        st.info("💡 Login to access your cart, favorites, and order history!")
    
    # Search area
    st.markdown("#### 🔍 Search Products")
    search_col1, search_col2, search_col3 = st.columns(3)
    
    with search_col1:
        search_term = st.text_input("Search by name (e.g., 'sun', 'table')", placeholder="Enter product name...")
    
    with search_col2:
        price_filter = st.selectbox("Price Filter", ["All", "< $50", "$50-$100", "$100-$200", "> $200"])
    
    with search_col3:
        stock_filter = st.selectbox("Stock Filter", ["All", "In Stock (>0)", "Low Stock (<10)", "High Stock (>50)"])
    
    # Get and filter products
    products = get_products()
    
    if not products:
        st.warning("No products available")
        return
    
    # Convert to DataFrame for easier filtering
    df = pd.DataFrame(products, columns=['ID', 'Name', 'Description', 'Price', 'Category', 'Stock', 'Rating'])
    
    # Apply filters
    filtered_df = df.copy()
    
    # Name search filter
    if search_term:
        search_terms = [term.strip().lower() for term in search_term.split(',')]
        mask = filtered_df['Name'].str.lower().str.contains('|'.join(search_terms), na=False)
        filtered_df = filtered_df[mask]
    
    # Price filter
    if price_filter != "All":
        if price_filter == "< $50":
            filtered_df = filtered_df[filtered_df['Price'] < 50]
        elif price_filter == "$50-$100":
            filtered_df = filtered_df[(filtered_df['Price'] >= 50) & (filtered_df['Price'] <= 100)]
        elif price_filter == "$100-$200":
            filtered_df = filtered_df[(filtered_df['Price'] >= 100) & (filtered_df['Price'] <= 200)]
        elif price_filter == "> $200":
            filtered_df = filtered_df[filtered_df['Price'] > 200]
    
    # Stock filter
    if stock_filter != "All":
        if stock_filter == "In Stock (>0)":
            filtered_df = filtered_df[filtered_df['Stock'] > 0]
        elif stock_filter == "Low Stock (<10)":
            filtered_df = filtered_df[filtered_df['Stock'] < 10]
        elif stock_filter == "High Stock (>50)":
            filtered_df = filtered_df[filtered_df['Stock'] > 50]
    
    # Display results
    if filtered_df.empty:
        st.warning("🔍 No products found matching your search criteria.")
        st.info("Try adjusting your search terms or filters.")
    else:
        st.markdown(f"#### 📦 Available Items ({len(filtered_df)} products)")
        
        # Display products in grid format
        cols_per_row = 3
        for i in range(0, len(filtered_df), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, (idx, product) in enumerate(filtered_df.iloc[i:i+cols_per_row].iterrows()):
                if j < len(cols):
                    with cols[j]:
                        st.markdown(f"**{product['Name']}**")
                        st.write(f"💰 **${product['Price']:.2f}**")
                        st.write(f"📦 **Stock: {product['Stock']}**")
                        st.write(f"⭐ Rating: {product['Rating']}/5")
                        st.write(f"🏷️ {product['Category']}")
                        
                        # Action buttons - only show if logged in
                        if st.session_state.logged_in:
                            btn_col1, btn_col2 = st.columns(2)
                            with btn_col1:
                                if st.button(f"🛒 Add to Order", key=f"add_{product['ID']}"):
                                    if product['Stock'] > 0:
                                        success, message = add_item_to_temp_order(st.session_state.user_id, product['ID'])
                                        if success:
                                            st.success(message)
                                            st.rerun()
                                        else:
                                            st.error(message)
                                    else:
                                        st.error("Out of stock!")
                            
                            with btn_col2:
                                is_fav = is_favorite(st.session_state.user_id, product['ID'])
                                if st.button(f"{'💖' if is_fav else '🤍'} Fav", key=f"fav_{product['ID']}"):
                                    if is_fav:
                                        success, message = remove_from_favorites(st.session_state.user_id, product['ID'])
                                    else:
                                        success, message = add_to_favorites(st.session_state.user_id, product['ID'])
                                    
                                    if success:
                                        st.success(message)
                                        st.rerun()
                                    else:
                                        st.error(message)
                        else:
                            # Show login prompt for non-logged users
                            st.info("🔐 Login to add to cart and favorites")
                        
                        st.markdown("---")

def favorites_page():
    """User's favorite items page"""
    st.title("💖 My Favorite Items")
    
    favorites = get_user_favorites(st.session_state.user_id)
    
    if not favorites:
        st.info("No favorite items yet. Add some products to your favorites from the main page!")
        return
    
    st.markdown(f"#### You have {len(favorites)} favorite items")
    
    # Display favorites in same format as main page
    df = pd.DataFrame(favorites, columns=['ID', 'Name', 'Description', 'Price', 'Category', 'Stock', 'Rating'])
    
    cols_per_row = 3
    for i in range(0, len(df), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, (idx, product) in enumerate(df.iloc[i:i+cols_per_row].iterrows()):
            if j < len(cols):
                with cols[j]:
                    st.markdown(f"**{product['Name']}**")
                    st.write(f"💰 **${product['Price']:.2f}**")
                    st.write(f"📦 **Stock: {product['Stock']}**")
                    st.write(f"⭐ Rating: {product['Rating']}/5")
                    st.write(f"🏷️ {product['Category']}")
                    
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button(f"🛒 Add to Order", key=f"fav_add_{product['ID']}"):
                            if product['Stock'] > 0:
                                success, message = add_item_to_temp_order(st.session_state.user_id, product['ID'])
                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
                            else:
                                st.error("Out of stock!")
                    
                    with btn_col2:
                        if st.button("💔 Remove", key=f"fav_remove_{product['ID']}"):
                            success, message = remove_from_favorites(st.session_state.user_id, product['ID'])
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                    
                    st.markdown("---")

def order_page():
    """Order management page with TEMP/CLOSE orders"""
    st.title("📦 My Orders")
    
    # Get temp order
    temp_order = get_temp_order(st.session_state.user_id)
    
    # Get all orders
    all_orders = get_user_orders(st.session_state.user_id)
    
    if temp_order:
        st.markdown("### 🚧 Current Order (TEMP)")
        st.markdown("**Order Details:**")
        st.write(f"📅 Created: {temp_order['created_at']}")
        st.write(f"💰 Total: ${temp_order['total_amount']:.2f}")
        
        # Display items in temp order
        if temp_order['items']:
            st.markdown("**Items in Order:**")
            for item in temp_order['items']:
                product_id, name, quantity, price, stock = item
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.write(f"**{name}**")
                with col2:
                    st.write(f"Qty: {quantity}")
                with col3:
                    st.write(f"${price:.2f}")
                with col4:
                    if st.button("🗑️", key=f"remove_{product_id}"):
                        success, message = remove_item_from_temp_order(st.session_state.user_id, product_id)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
            
            # Shipping address and purchase
            st.markdown("**Complete Your Order:**")
            shipping_address = st.text_area("Shipping Address", 
                                           value=temp_order.get('shipping_address', ''),
                                           placeholder="Enter your full shipping address...")
            
            if st.button("💳 Purchase Order", type="primary"):
                if shipping_address.strip():
                    success, message = complete_order(st.session_state.user_id, shipping_address)
                    if success:
                        st.success(message)
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please enter a shipping address")
        else:
            st.info("Your order is empty")
        
        st.markdown("---")
    
    # Display order history
    st.markdown("### 📋 Order History")
    closed_orders = [order for order in all_orders if order[2] == 'CLOSE']
    
    if not closed_orders:
        st.info("No completed orders yet")
    else:
        for order in closed_orders:
            order_id, total_amount, status, shipping_address, created_at = order
            
            with st.expander(f"Order #{order_id} - ${total_amount:.2f} ({created_at})"):
                st.write(f"**Status:** {status}")
                st.write(f"**Total:** ${total_amount:.2f}")
                st.write(f"**Shipping Address:** {shipping_address}")
                st.write(f"**Date:** {created_at}")
                
                # Get order items
                items = get_order_items(order_id)
                if items:
                    st.markdown("**Items:**")
                    items_df = pd.DataFrame(items, columns=['Product ID', 'Name', 'Quantity', 'Price', 'Subtotal'])
                    st.dataframe(items_df, hide_index=True)

def chat_page():
    """ChatGPT assistant page with 5 prompt limit"""
    st.title("🤖 AI Chat Assistant")
    
    # Display prompt count
    remaining_prompts = 5 - st.session_state.chat_prompts_count
    if remaining_prompts > 0:
        st.success(f"You have {remaining_prompts} prompts remaining this session")
    else:
        st.error("You have used all 5 prompts for this session. Please logout and login again to reset.")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 💬 Chat History")
        for i, (user_msg, ai_msg) in enumerate(st.session_state.chat_history):
            st.markdown(f"**You:** {user_msg}")
            st.markdown(f"**AI Assistant:** {ai_msg}")
            st.markdown("---")
    
    # Chat input
    if remaining_prompts > 0:
        user_question = st.text_area("Ask about our products:", 
                                    placeholder="e.g., 'What is the average size of a basketball?'",
                                    height=100)
        
        if st.button("Send Question", type="primary"):
            if user_question.strip():
                # Get products for context
                products = get_products()
                product_context = ""
                if products:
                    product_list = [f"- {p[1]}: ${p[3]:.2f}, Stock: {p[5]}" for p in products[:10]]
                    product_context = "Available products:\n" + "\n".join(product_list)
                
                # Get AI response
                try:
                    context = f"You are a helpful shopping assistant. Answer questions about these products: {product_context}\n\nUser question: {user_question}"
                    ai_response = get_chatbot_response(context)
                    
                    # Update session state
                    st.session_state.chat_history.append((user_question, ai_response))
                    st.session_state.chat_prompts_count += 1
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Sorry, the chat assistant is not available right now: {str(e)}")
            else:
                st.error("Please enter a question")
    else:
        st.info("Chat limit reached. Login again to reset your prompt count.")

def user_menu():
    """User menu in sidebar"""
    with st.sidebar:
        if st.session_state.logged_in:
            user = st.session_state.user_info
            st.success(f"👤 Welcome, {user['first_name']} {user['last_name']}")
            st.write(f"**Username:** {user['username']}")
            
            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.session_state.user_id = None
                st.session_state.user_info = None
                st.session_state.chat_prompts_count = 0
                st.session_state.chat_history = []
                st.rerun()
            
            if st.button("🗑️ Delete Account", type="secondary"):
                if st.checkbox("I confirm I want to delete my account permanently"):
                    success, message = delete_user_account(st.session_state.user_id)
                    if success:
                        st.success(message)
                        st.session_state.logged_in = False
                        st.session_state.user_id = None
                        st.session_state.user_info = None
                        st.rerun()
                    else:
                        st.error(message)

def navigation():
    """Page navigation"""
    if st.session_state.logged_in:
        st.markdown("### 🧭 Navigation")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🏠 Main Page", use_container_width=True):
                st.session_state.current_page = "Main"
                st.rerun()
        
        with col2:
            if st.button("📦 Orders", use_container_width=True):
                st.session_state.current_page = "Orders"
                st.rerun()
        
        with col3:
            if st.button("💖 Favorites", use_container_width=True):
                st.session_state.current_page = "Favorites"
                st.rerun()
        
        with col4:
            if st.button("🤖 AI Chat", use_container_width=True):
                st.session_state.current_page = "Chat"
                st.rerun()

def main():
    """Main application with enhanced navigation"""
    # Enhanced Navigation Header
    st.markdown("---")
    
    # Top navigation bar with login/register buttons
    nav_col1, nav_col2, nav_col3 = st.columns([6, 1, 1])
    
    with nav_col1:
        # Main navigation buttons
        if st.session_state.logged_in:
            # Navigation for logged in users
            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
            
            with col1:
                if st.button("🏠 Main", key="nav_main"):
                    st.session_state.current_page = "Main"
                    st.rerun()
            
            with col2:
                if st.button("📦 Orders", key="nav_orders"):
                    st.session_state.current_page = "Orders" 
                    st.rerun()
            
            with col3:
                if st.button("💖 Favorites", key="nav_favorites"):
                    st.session_state.current_page = "Favorites"
                    st.rerun()
            
            with col4:
                if st.button("💬 Chat", key="nav_chat"):
                    st.session_state.current_page = "Chat"
                    st.rerun()
        else:
            # Simple navigation for non-logged users
            if st.button("🏠 Browse Products", key="nav_main_guest"):
                st.session_state.current_page = "Main"
                st.rerun()
    
    with nav_col2:
        if not st.session_state.logged_in:
            if st.button("🔐 Login", key="show_login"):
                st.session_state.current_page = "Login"
                st.rerun()
        else:
            st.write(f"👋 {st.session_state.user_info['first_name']}")
    
    with nav_col3:
        if not st.session_state.logged_in:
            if st.button("📝 Register", key="show_register"):
                st.session_state.current_page = "Register"
                st.rerun()
        else:
            if st.button("🚪 Logout", key="nav_logout"):
                # Reset session state
                st.session_state.logged_in = False
                st.session_state.user_id = None
                st.session_state.user_info = None
                st.session_state.current_page = "Main"
                st.session_state.chat_prompts_count = 0
                st.session_state.chat_history = []
                st.rerun()
    
    st.markdown("---")
    
    # User menu in sidebar for logged in users
    if st.session_state.logged_in:
        user_menu()
    
    # Page routing - Always show content based on current page
    if st.session_state.current_page == "Login":
        login_page()
    elif st.session_state.current_page == "Register":
        register_page()
    elif st.session_state.current_page == "Main":
        main_page()
    elif st.session_state.current_page == "Orders":
        if st.session_state.logged_in:
            order_page()
        else:
            st.warning("Please login to view your orders")
            login_page()
    elif st.session_state.current_page == "Favorites":
        if st.session_state.logged_in:
            favorites_page()
        else:
            st.warning("Please login to view your favorites")
            login_page()
    elif st.session_state.current_page == "Chat":
        if st.session_state.logged_in:
            chat_page()
        else:
            st.warning("Please login to use the chat assistant")
            login_page()

def register_page():
    """Dedicated registration page"""
    st.title("📝 Create New Account")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
        
        with col2:
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            country = st.text_input("Country")
            city = st.text_input("City")
        
        submit = st.form_submit_button("Create Account", type="primary")
        
        if submit:
            if all([first_name, last_name, username, password, email, phone, country, city]):
                success, message = create_user(
                    first_name, last_name, username, password, 
                    email, phone, country, city
                )
                if success:
                    st.success(message)
                    st.info("Account created successfully! You can now login.")
                    if st.button("Go to Login"):
                        st.session_state.current_page = "Login"
                        st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please fill in all fields")

if __name__ == "__main__":
    main()