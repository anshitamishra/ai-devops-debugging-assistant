import streamlit as st
from utils.k8s_monitor import get_cluster_health

st.set_page_config(layout="wide")

st.title("Kubernetes Cluster Health")

cluster = get_cluster_health()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Healthy Nodes", cluster["nodes"])

with col2:
    st.metric("Running Pods", cluster["pods"])

with col3:
    st.metric("Cluster Status", cluster["status"])

st.success("Real-time Kubernetes monitoring enabled.")