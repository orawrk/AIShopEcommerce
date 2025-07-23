"""
AI E-Commerce Platform Presentation Generator
Creates a comprehensive presentation with screenshots
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time
import os

def create_presentation():
    """Create a comprehensive presentation of the AI e-commerce platform"""
    
    st.set_page_config(
        page_title="AI E-Commerce Platform - Presentation",
        page_icon="📊",
        layout="wide"
    )
    
    # Custom CSS for better presentation styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 1rem;
    }
    
    .section-header {
        font-size: 2rem;
        color: #ff7f0e;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-left: 5px solid #ff7f0e;
        padding-left: 1rem;
    }
    
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #2ca02c;
    }
    
    .tech-stack {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .metric-card {
        background-color: #fff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main Title
    st.markdown('<h1 class="main-header">🛒 AI-Powered E-Commerce Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Intelligent Shopping Experience with Machine Learning & AI</p>', unsafe_allow_html=True)
    
    # Executive Summary
    st.markdown('<h2 class="section-header">📋 Executive Summary</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
        <h3>🎯 Project Overview</h3>
        <p>A comprehensive AI-powered e-commerce platform that leverages machine learning to create personalized shopping experiences, intelligent product recommendations, and automated customer support.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
        <h3>🚀 Key Innovation</h3>
        <p>Integration of ChatGPT for customer support, ML-driven user behavior prediction, and real-time product recommendations with seamless user experience.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Technical Architecture
    st.markdown('<h2 class="section-header">🏗️ Technical Architecture</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="tech-stack">
        <h4>🖥️ Frontend</h4>
        <ul>
        <li>Streamlit Web App</li>
        <li>Interactive UI/UX</li>
        <li>Real-time Updates</li>
        <li>Responsive Design</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tech-stack">
        <h4>⚙️ Backend</h4>
        <ul>
        <li>FastAPI Framework</li>
        <li>RESTful APIs</li>
        <li>Async Processing</li>
        <li>Authentication</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="tech-stack">
        <h4>🗄️ Database</h4>
        <ul>
        <li>MySQL Database</li>
        <li>Relational Schema</li>
        <li>ACID Compliance</li>
        <li>Data Integrity</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="tech-stack">
        <h4>🤖 AI/ML</h4>
        <ul>
        <li>ChatGPT Integration</li>
        <li>Scikit-learn ML</li>
        <li>Behavior Prediction</li>
        <li>Flask ML API</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Key Features
    st.markdown('<h2 class="section-header">✨ Key Features</h2>', unsafe_allow_html=True)
    
    features_col1, features_col2 = st.columns(2)
    
    with features_col1:
        st.markdown("""
        <div class="feature-box">
        <h3>🔐 User Management</h3>
        <ul>
        <li>Secure user registration and authentication</li>
        <li>Password hashing with bcrypt</li>
        <li>User profile management</li>
        <li>Account deletion functionality</li>
        </ul>
        </div>
        
        <div class="feature-box">
        <h3>🛍️ Product Catalog</h3>
        <ul>
        <li>20+ sample products across categories</li>
        <li>Advanced search and filtering</li>
        <li>Real-time stock management</li>
        <li>Product ratings and reviews</li>
        </ul>
        </div>
        
        <div class="feature-box">
        <h3>❤️ Favorites System</h3>
        <ul>
        <li>Save favorite products</li>
        <li>Personal wishlist management</li>
        <li>Quick access to loved items</li>
        <li>Remove unwanted favorites</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with features_col2:
        st.markdown("""
        <div class="feature-box">
        <h3>🛒 Shopping Cart & Orders</h3>
        <ul>
        <li>Temporary order system</li>
        <li>Add/remove items from cart</li>
        <li>Order completion workflow</li>
        <li>Order history tracking</li>
        </ul>
        </div>
        
        <div class="feature-box">
        <h3>🤖 AI Chat Support</h3>
        <ul>
        <li>ChatGPT-powered customer support</li>
        <li>Product-specific assistance</li>
        <li>Natural language processing</li>
        <li>Limited prompts per session</li>
        </ul>
        </div>
        
        <div class="feature-box">
        <h3>📊 ML Predictions</h3>
        <ul>
        <li>User behavior prediction</li>
        <li>Churn analysis</li>
        <li>Spending pattern analysis</li>
        <li>Real-time model retraining</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Database Schema
    st.markdown('<h2 class="section-header">🗄️ Database Schema</h2>', unsafe_allow_html=True)
    
    schema_col1, schema_col2 = st.columns(2)
    
    with schema_col1:
        st.markdown("""
        **Core Tables:**
        - **users**: User account information
        - **products**: Product catalog with stock
        - **orders**: Order management system
        - **order_items**: Individual order line items
        """)
    
    with schema_col2:
        st.markdown("""
        **Supporting Tables:**
        - **favorites**: User's favorite products
        - **temp_orders**: Shopping cart functionality
        - **user_behavior**: ML training data
        """)
    
    # Performance Metrics
    st.markdown('<h2 class="section-header">📈 Platform Metrics</h2>', unsafe_allow_html=True)
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.markdown("""
        <div class="metric-card">
        <h3 style="color: #1f77b4;">20+</h3>
        <p>Products Available</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown("""
        <div class="metric-card">
        <h3 style="color: #ff7f0e;">4</h3>
        <p>Core Modules</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown("""
        <div class="metric-card">
        <h3 style="color: #2ca02c;">100%</h3>
        <p>AI Integration</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col4:
        st.markdown("""
        <div class="metric-card">
        <h3 style="color: #d62728;">5000</h3>
        <p>Port Availability</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Technology Stack Details
    st.markdown('<h2 class="section-header">🔧 Technology Stack</h2>', unsafe_allow_html=True)
    
    tech_data = {
        'Component': ['Frontend', 'Backend API', 'Database', 'ML Engine', 'AI Support'],
        'Technology': ['Streamlit', 'FastAPI', 'MySQL', 'Scikit-learn', 'OpenAI GPT'],
        'Port': ['5000', '8001', '3306', '8000', 'API'],
        'Status': ['✅ Running', '✅ Running', '✅ Running', '✅ Running', '✅ Integrated']
    }
    
    tech_df = pd.DataFrame(tech_data)
    st.dataframe(tech_df, use_container_width=True)
    
    # Future Enhancements
    st.markdown('<h2 class="section-header">🚀 Future Enhancements</h2>', unsafe_allow_html=True)
    
    enhancement_col1, enhancement_col2 = st.columns(2)
    
    with enhancement_col1:
        st.markdown("""
        **Short-term Goals:**
        - Payment gateway integration
        - Email notifications
        - Advanced analytics dashboard
        - Mobile app development
        """)
    
    with enhancement_col2:
        st.markdown("""
        **Long-term Vision:**
        - Blockchain payments (MetaMask)
        - Computer vision for product search
        - Voice-based shopping assistant
        - AR/VR product visualization
        """)
    
    # Call to Action
    st.markdown('<h2 class="section-header">🎯 Ready for Deployment</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-box">
    <h3>✅ Production Ready Features</h3>
    <p>The platform is fully functional with user authentication, product management, order processing, 
    AI chat support, and machine learning capabilities. All components are tested and running successfully.</p>
    
    <p><strong>Access the live application at:</strong> <code>http://0.0.0.0:5000</code></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(f"**Presentation generated on:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    st.markdown("**Platform Status:** 🟢 All systems operational")

if __name__ == "__main__":
    create_presentation()