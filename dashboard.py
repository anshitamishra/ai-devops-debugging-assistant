import json
import os
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="AI DevOps Dashboard",
    page_icon="🚨",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: white;
}

.metric-card {
    background-color: #1E293B;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 0px 12px rgba(0,255,255,0.2);
}

.metric-title {
    color: #94A3B8;
    font-size: 18px;
}

.metric-value {
    color: white;
    font-size: 35px;
    font-weight: bold;
}

.section-box {
    background-color: #111827;
    padding: 20px;
    border-radius: 15px;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# TITLE
# =========================================
st.title("AI DevOps Incident Intelligence Dashboard")

st.markdown(
    """
Monitor Kubernetes and CI/CD infrastructure incidents
using hybrid AI-powered operational analytics.
"""
)

# =========================================
# SIDEBAR
# =========================================
st.sidebar.title("AI Ops Control Panel")

st.sidebar.info(
    """
This dashboard provides:

- Incident analytics
- Severity tracking
- AI operational insights
- Kubernetes issue monitoring
- Recurring incident detection
"""
)

# =========================================
# LOAD INCIDENT HISTORY
# =========================================
DATA_FILE = "data/incidents.json"

if not os.path.exists(DATA_FILE):

    st.error("No incident history found.")

    st.stop()

with open(DATA_FILE, "r") as file:

    incidents = json.load(file)

# =========================================
# CREATE DATAFRAME
# =========================================
rows = []

for item in incidents:

    for issue in item["issues"]:

        rows.append({
            "Incident ID": item["incident_id"],
            "Severity": item["severity"],
            "Issue": issue,
            "Source": item["source"]
        })

df = pd.DataFrame(rows)

# =========================================
# METRICS
# =========================================
st.subheader("Operational Metrics")

col1, col2, col3, col4 = st.columns(4)

critical_count = len(df[df["Severity"] == "CRITICAL"])

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Incidents</div>
        <div class="metric-value">{len(df)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Incident Types</div>
        <div class="metric-value">{df['Issue'].nunique()}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Critical Incidents</div>
        <div class="metric-value">{critical_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Infrastructure Sources</div>
        <div class="metric-value">{df['Source'].nunique()}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# INCIDENT TABLE
# =========================================
st.subheader("Incident History")

st.markdown('<div class="section-box">', unsafe_allow_html=True)

st.dataframe(df, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# CHARTS
# =========================================
left, right = st.columns(2)

# =========================================
# INCIDENT DISTRIBUTION
# =========================================
with left:

    st.subheader("Incident Distribution")

    issue_counts = Counter(df["Issue"])

    fig, ax = plt.subplots(figsize=(5, 4))

    ax.bar(issue_counts.keys(), issue_counts.values())

    plt.xticks(rotation=15)

    st.pyplot(fig)

# =========================================
# SEVERITY DISTRIBUTION
# =========================================
with right:

    st.subheader("Severity Distribution")

    severity_counts = Counter(df["Severity"])

    fig2, ax2 = plt.subplots(figsize=(5, 4))

    ax2.pie(
        severity_counts.values(),
        labels=severity_counts.keys(),
        autopct="%1.1f%%"
    )

    st.pyplot(fig2)

# =========================================
# RECURRING INCIDENTS
# =========================================
st.subheader("Recurring Infrastructure Failures")

for issue, count in issue_counts.items():

    if count >= 2:

        st.warning(
            f"{issue} occurred {count} times across recent incidents."
        )

# =========================================
# AI INSIGHTS
# =========================================
st.subheader("AI Operational Insights")

most_common = issue_counts.most_common(1)

if most_common:

    issue_name = most_common[0][0]

    issue_count = most_common[0][1]

    st.success(
        f"""
        Most recurring operational issue detected:
        {issue_name}

        Total Occurrences: {issue_count}
        """
    )

# =========================================
# FOOTER
# =========================================
st.markdown("---")

st.caption(
    "AI DevOps Debugging Assistant | Hybrid Incident Detection Platform"
)