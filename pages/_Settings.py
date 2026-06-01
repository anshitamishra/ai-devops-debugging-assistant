import streamlit as st

st.set_page_config(
    page_title="Settings",
    layout="wide"
)

st.title("Platform Settings")

st.markdown("""
Configure AI analysis and infrastructure monitoring preferences.
""")

st.toggle("Enable AI Monitoring", value=True)

st.toggle("Enable Auto Remediation", value=False)

st.toggle("Enable Incident Alerts", value=True)

st.selectbox(
    "AI Analysis Mode",
    [
        "Hybrid AI + Rule Engine",
        "AI Only",
        "Rule-Based Only"
    ]
)

st.slider(
    "AI Confidence Threshold",
    0,
    100,
    85
)

st.button("Save Configuration")