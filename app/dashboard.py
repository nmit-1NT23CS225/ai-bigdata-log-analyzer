import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configuration
st.set_page_config(page_title="Big Data Log Analyzer", layout="wide", page_icon="📊")
API_URL = "http://127.0.0.1:8000/analyze"

st.title("🚀 AI-Powered Big Data Log Analyzer")
st.markdown("Upload your server logs to perform PySpark processing and detect anomalous IP activity using Isolation Forest.")

st.sidebar.header("1. Upload Log File")
uploaded_file = st.sidebar.file_uploader("Choose a log file", type=['log', 'txt'])

if uploaded_file is not None:
    if st.sidebar.button("Run Analysis Engine"):
        with st.spinner("Processing large-scale logs via PySpark & Scikit-Learn..."):
            try:
                # Send file to FastAPI backend
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/plain")}
                response = requests.post(API_URL, files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success("Analysis Complete!")
                    
                    # --- Section 1: KPI Summary ---
                    st.header("📊 Overview")
                    col1, col2, col3, col4, col5 = st.columns(5)
                    summary = data.get('summary', {})
                    
                    col1.metric("Total Logs", f"{summary.get('total_logs_analyzed', 0):,}")
                    col2.metric("Unique IPs", f"{summary.get('total_unique_ips', 0):,}")
                    col3.metric("Anomalous IPs", f"{summary.get('total_anomalies_found', 0)}")
                    col4.metric("Peak Hour", f"{summary.get('peak_traffic_hour', 'N/A')}:00")
                    col5.metric("Error Rate", f"{summary.get('overall_error_rate', 0):.2%}")
                    
                    st.divider()
                    
                    # --- Section 2: Anomalies ---
                    st.header("🚨 Suspicious Activity Detected")
                    suspicious_ips = data.get('suspicious_ips', [])
                    if suspicious_ips:
                        df_anomalies = pd.DataFrame(suspicious_ips)
                        # Format the ratio
                        df_anomalies['error_ratio'] = df_anomalies['error_ratio'].apply(lambda x: f"{x:.2%}")
                        st.dataframe(df_anomalies, use_container_width=True)
                    else:
                        st.info("No suspicious IPs detected.")
                    
                    st.divider()
                    
                    # --- Section 3: Traffic Analysis ---
                    col_left, col_right = st.columns(2)
                    
                    with col_left:
                        st.header("🔝 Top 10 IPs by Traffic")
                        top_ips = data.get('top_ips', [])
                        if top_ips:
                            df_top_ips = pd.DataFrame(top_ips)
                            fig1 = px.bar(df_top_ips, x='ip', y='total_requests', 
                                         color='error_count', 
                                         title="Traffic Volume per IP (Color = Errors)")
                            st.plotly_chart(fig1, use_container_width=True)
                            
                    with col_right:
                        st.header("🎯 Top Accessed Endpoints")
                        top_endpoints = data.get('top_endpoints', [])
                        if top_endpoints:
                            df_endpoints = pd.DataFrame(top_endpoints)
                            fig2 = px.pie(df_endpoints, names='endpoint', values='count', 
                                         title="Endpoint Distribution")
                            st.plotly_chart(fig2, use_container_width=True)

                else:
                    st.error(f"Backend Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}. Is the FastAPI server running?")
else:
    st.info("Please upload a log file from the sidebar to begin.")
    st.markdown("Don't have one? Run `python data/generate_logs.py` to create a sample.")
