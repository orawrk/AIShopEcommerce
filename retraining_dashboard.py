"""
Real-time Model Retraining Dashboard Component

This module provides a comprehensive dashboard interface for monitoring and controlling
the real-time machine learning model retraining system in the AI e-commerce platform.

Features:
- Real-time status monitoring
- Performance metrics visualization
- Manual retraining controls
- Training history tracking
- Configuration management

Author: AI E-Commerce Platform Team
Version: 1.0.0
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time

def show_retraining_dashboard():
    """Display comprehensive real-time retraining dashboard"""
    
    st.header("🔄 Real-time Model Retraining Dashboard")
    st.markdown("Monitor and control automated machine learning model updates based on new user data")
    
    # Service Status Section
    st.subheader("📊 Service Status")
    
    try:
        # Get retraining status from ML API
        response = requests.get("http://localhost:8000/retraining/status", timeout=5)
        
        if response.status_code == 200:
            status_data = response.json().get('retraining', {})
            
            # Status metrics in columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                is_running = status_data.get('running', False)
                status_icon = "🟢" if is_running else "🔴"
                status_text = "Active" if is_running else "Inactive"
                st.metric("Service Status", f"{status_icon} {status_text}")
            
            with col2:
                new_samples = status_data.get('new_samples', 0)
                min_needed = status_data.get('min_samples_needed', 100)
                progress = min(new_samples / min_needed, 1.0) if min_needed > 0 else 0
                st.metric("Data Progress", f"{new_samples}/{min_needed}")
                st.progress(progress)
            
            with col3:
                last_retrain = status_data.get('last_retrain', 'Never')
                if last_retrain != 'Never':
                    try:
                        dt = datetime.fromisoformat(last_retrain.replace('Z', '+00:00'))
                        time_ago = datetime.now() - dt.replace(tzinfo=None)
                        if time_ago.days > 0:
                            formatted_time = f"{time_ago.days}d ago"
                        elif time_ago.seconds > 3600:
                            formatted_time = f"{time_ago.seconds//3600}h ago"
                        else:
                            formatted_time = f"{time_ago.seconds//60}m ago"
                        st.metric("Last Retrain", formatted_time)
                    except:
                        st.metric("Last Retrain", "Recent")
                else:
                    st.metric("Last Retrain", "Never")
            
            with col4:
                next_check = status_data.get('next_check_in_hours', 24)
                st.metric("Next Check", f"{next_check}h")
            
            # Control Panel
            st.subheader("🎛️ Control Panel")
            
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if st.button("🟢 Start Auto-Retraining", use_container_width=True):
                    with st.spinner("Starting auto-retraining service..."):
                        try:
                            response = requests.post("http://localhost:8000/retraining/start")
                            if response.status_code == 200:
                                st.success("Auto-retraining service started successfully!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Failed to start auto-retraining service")
                        except Exception as e:
                            st.error(f"Connection error: {e}")
            
            with col_btn2:
                if st.button("🔴 Stop Auto-Retraining", use_container_width=True):
                    with st.spinner("Stopping auto-retraining service..."):
                        try:
                            response = requests.post("http://localhost:8000/retraining/stop")
                            if response.status_code == 200:
                                st.success("Auto-retraining service stopped successfully!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Failed to stop auto-retraining service")
                        except Exception as e:
                            st.error(f"Connection error: {e}")
            
            with col_btn3:
                if st.button("⚡ Force Retrain Now", use_container_width=True):
                    with st.spinner("Initiating immediate model retraining..."):
                        try:
                            response = requests.post("http://localhost:8000/retraining/force")
                            if response.status_code == 200:
                                result = response.json()
                                if result.get('status') == 'success':
                                    st.success("Models retrained successfully!")
                                    st.balloons()
                                else:
                                    st.warning("Retraining completed with warnings")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Model retraining failed")
                        except Exception as e:
                            st.error(f"Connection error: {e}")
            
            # Detailed Configuration
            with st.expander("⚙️ Configuration Details"):
                config_col1, config_col2 = st.columns(2)
                
                with config_col1:
                    st.write("**Retraining Triggers:**")
                    st.write(f"• Minimum new samples: {status_data.get('min_samples_needed', 'N/A')}")
                    st.write(f"• Check interval: {status_data.get('next_check_in_hours', 'N/A')} hours")
                    st.write(f"• Performance threshold: 5% improvement")
                
                with config_col2:
                    st.write("**Current Status:**")
                    st.write(f"• Service running: {'Yes' if status_data.get('running') else 'No'}")
                    st.write(f"• New samples: {status_data.get('new_samples', 0)}")
                    st.write(f"• History records: {status_data.get('performance_history_length', 0)}")
            
            # Performance Monitoring Section
            st.subheader("📈 Performance Monitoring")
            
            # Try to load performance history
            try:
                with open('performance_history.json', 'r') as f:
                    performance_history = json.load(f)
                
                if performance_history:
                    # Convert to DataFrame for visualization
                    df_perf = pd.DataFrame(performance_history)
                    df_perf['timestamp'] = pd.to_datetime(df_perf['timestamp'])
                    
                    # Performance metrics chart
                    fig_perf = go.Figure()
                    
                    fig_perf.add_trace(go.Scatter(
                        x=df_perf['timestamp'],
                        y=df_perf['accuracy'],
                        mode='lines+markers',
                        name='Model Accuracy',
                        line=dict(color='#1f77b4', width=2),
                        marker=dict(size=6)
                    ))
                    
                    fig_perf.update_layout(
                        title='Model Performance Over Time',
                        xaxis_title='Time',
                        yaxis_title='Accuracy',
                        hovermode='x unified',
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig_perf, use_container_width=True)
                    
                    # Performance summary
                    latest_perf = performance_history[-1]
                    col_perf1, col_perf2, col_perf3 = st.columns(3)
                    
                    with col_perf1:
                        st.metric(
                            "Latest Accuracy", 
                            f"{latest_perf['accuracy']:.3f}",
                            delta=f"{latest_perf['accuracy'] - performance_history[-2]['accuracy']:.3f}" if len(performance_history) > 1 else None
                        )
                    
                    with col_perf2:
                        st.metric(
                            "Latest MSE", 
                            f"{latest_perf['mse']:.2f}",
                            delta=f"{latest_perf['mse'] - performance_history[-2]['mse']:.2f}" if len(performance_history) > 1 else None
                        )
                    
                    with col_perf3:
                        st.metric(
                            "Training Samples", 
                            f"{latest_perf.get('samples_used', 'N/A')}"
                        )
                
                else:
                    st.info("No performance history available yet. Performance data will appear after the first retraining.")
                    
            except FileNotFoundError:
                st.info("Performance history file not found. Data will be available after first retraining cycle.")
            except Exception as e:
                st.warning(f"Could not load performance history: {e}")
            
            # Data Quality Monitoring
            st.subheader("🔍 Data Quality Monitoring")
            
            # Simulate data quality metrics (in real implementation, get from database)
            data_quality_col1, data_quality_col2, data_quality_col3 = st.columns(3)
            
            with data_quality_col1:
                st.metric("Data Completeness", "94.2%", delta="2.1%")
            
            with data_quality_col2:
                st.metric("Feature Stability", "Good", delta="Stable")
            
            with data_quality_col3:
                st.metric("Data Freshness", "< 1h", delta="Real-time")
            
            # Recommendations
            st.subheader("💡 Recommendations")
            
            if new_samples >= min_needed:
                st.success("✅ Sufficient new data available for retraining")
            elif new_samples > min_needed * 0.5:
                st.warning(f"⚠️ Approaching retraining threshold ({new_samples}/{min_needed} samples)")
            else:
                st.info(f"ℹ️ Collecting more data for next retraining cycle ({new_samples}/{min_needed} samples)")
            
            if not is_running:
                st.warning("⚠️ Auto-retraining service is not running. Consider starting it for continuous model updates.")
        
        else:
            st.error("Failed to fetch retraining status from ML API")
            _show_fallback_interface()
    
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to ML API service")
        _show_fallback_interface()
    
    except requests.exceptions.Timeout:
        st.error("⏱️ ML API request timed out")
        _show_fallback_interface()
    
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        _show_fallback_interface()

def _show_fallback_interface():
    """Show fallback interface when ML API is unavailable"""
    st.subheader("🛠️ Manual Model Management")
    st.info("Real-time retraining service is currently unavailable. You can still perform manual model operations.")
    
    col_fallback1, col_fallback2 = st.columns(2)
    
    with col_fallback1:
        if st.button("🔄 Manual Retrain", use_container_width=True):
            with st.spinner("Attempting manual model retraining..."):
                try:
                    response = requests.post("http://localhost:8000/retrain", timeout=30)
                    if response.status_code == 200:
                        st.success("Manual retraining completed successfully!")
                    else:
                        st.error("Manual retraining failed")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col_fallback2:
        if st.button("📊 Check Model Info", use_container_width=True):
            try:
                response = requests.get("http://localhost:8000/model-info", timeout=10)
                if response.status_code == 200:
                    model_info = response.json()
                    st.json(model_info)
                else:
                    st.error("Could not fetch model information")
            except Exception as e:
                st.error(f"Error: {e}")

def show_training_history():
    """Show detailed training history and analytics"""
    st.subheader("📜 Training History")
    
    try:
        with open('performance_history.json', 'r') as f:
            history = json.load(f)
        
        if history:
            df = pd.DataFrame(history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Training frequency chart
            fig_freq = px.histogram(
                df, 
                x=df['timestamp'].dt.date,
                title="Training Frequency Over Time",
                labels={'x': 'Date', 'y': 'Number of Retrainings'}
            )
            st.plotly_chart(fig_freq, use_container_width=True)
            
            # Performance trends
            fig_trends = go.Figure()
            
            fig_trends.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['accuracy'],
                mode='lines+markers',
                name='Accuracy',
                yaxis='y'
            ))
            
            fig_trends.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['mse'],
                mode='lines+markers',
                name='MSE',
                yaxis='y2'
            ))
            
            fig_trends.update_layout(
                title='Model Performance Trends',
                xaxis_title='Time',
                yaxis=dict(title='Accuracy', side='left'),
                yaxis2=dict(title='MSE', side='right', overlaying='y'),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_trends, use_container_width=True)
            
            # Summary statistics
            st.subheader("📊 Performance Summary")
            
            summary_col1, summary_col2, summary_col3 = st.columns(3)
            
            with summary_col1:
                avg_accuracy = df['accuracy'].mean()
                st.metric("Average Accuracy", f"{avg_accuracy:.3f}")
            
            with summary_col2:
                accuracy_improvement = df['accuracy'].iloc[-1] - df['accuracy'].iloc[0] if len(df) > 1 else 0
                st.metric("Total Improvement", f"{accuracy_improvement:.3f}")
            
            with summary_col3:
                total_retrainings = len(df)
                st.metric("Total Retrainings", total_retrainings)
        
        else:
            st.info("No training history available yet.")
    
    except FileNotFoundError:
        st.info("Training history will be available after the first retraining cycle.")
    except Exception as e:
        st.error(f"Error loading training history: {e}")

if __name__ == "__main__":
    # For testing the dashboard component
    show_retraining_dashboard()