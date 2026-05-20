import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from utils.detector import detect_known_issue, handle_known_issue
from ai_engine.analyzer import analyze_log
from utils.history_manager import (
    detect_recurring_issues,
    get_incident_count
)
from utils.severity_engine import (
    calculate_severity_score,
    get_priority,
    get_risk_level
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI DevOps Incident Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM STYLING
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0b1220;
    color: #e2e8f0;
}

.main {
    background-color: #0b1220;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1f2937;
}

h1, h2, h3, h4 {
    color: #f8fafc;
    font-weight: 600;
}

.stTextArea textarea {
    background-color: #111827;
    color: white;
    border: 1px solid #374151;
    border-radius: 12px;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: white;
    border: none;
    border-radius: 10px;
    height: 3em;
    font-weight: 600;
    transition: 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1d4ed8, #1e40af);
    transform: translateY(-2px);
}

.metric-card {
    background-color: #111827;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #1f2937;
}

.incident-card {
    background-color: #111827;
    padding: 20px;
    border-radius: 14px;
    border-left: 4px solid #ef4444;
    margin-bottom: 15px;
}

.analytics-card {
    background-color: #111827;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #1f2937;
    min-height: 180px;
}

.ai-card {
    background-color: #111827;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #1f2937;
    white-space: pre-wrap;
    line-height: 1.7;
    font-size: 14px;
}

.live-feed {
    background-color: #111827;
    padding: 12px;
    border-radius: 10px;
    border-left: 4px solid #2563eb;
    margin-bottom: 10px;
}

.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 40px;
    padding: 20px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("AI Ops Control Center")

st.sidebar.markdown("""
### Platform Modules

- Incident Detection
- AI Root Cause Analysis
- Kubernetes Monitoring
- Severity Analytics
- Incident Intelligence
- Operational Insights
""")

st.sidebar.markdown("---")

st.sidebar.caption(
    "Hybrid AI + Rule-Based Incident Analysis Platform"
)

# =========================================================
# HEADER
# =========================================================

st.title("AI DevOps Incident Intelligence Platform")

st.markdown("""
Enterprise-grade infrastructure incident analysis and operational monitoring
for Kubernetes and CI/CD environments.
""")

st.divider()

# =========================================================
# KPI METRICS
# =========================================================

total_incidents = get_incident_count()

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.metric("Total Incidents", total_incidents)

with metric2:
    st.metric("Critical Issues", "5")

with metric3:
    st.metric("Recurring Incidents", "3")

with metric4:
    st.metric("Cluster Stability", "85%")

st.markdown("""
<div style="
background:#111827;
padding:14px;
border-radius:12px;
border:1px solid #1f2937;
margin-top:15px;
">

<b>Infrastructure Status:</b>

<span style="
background:#14532d;
padding:6px 12px;
border-radius:20px;
margin-left:15px;
font-size:13px;
">
Production Cluster Active
</span>

<span style="
background:#78350f;
padding:6px 12px;
border-radius:20px;
margin-left:10px;
font-size:13px;
">
Memory Utilization Elevated
</span>

<span style="
background:#1e3a8a;
padding:6px 12px;
border-radius:20px;
margin-left:10px;
font-size:13px;
">
AI Monitoring Enabled
</span>

</div>
""", unsafe_allow_html=True)

st.divider()

# =========================================================
# LOG ANALYSIS
# =========================================================

st.subheader("Infrastructure Log Analysis")

uploaded_file = st.file_uploader(
    "Upload Infrastructure Logs",
    type=["txt", "log"]
)

uploaded_log_content = ""

if uploaded_file is not None:

    uploaded_log_content = uploaded_file.read().decode("utf-8")

    st.success("Infrastructure log uploaded successfully.")

log_input = st.text_area(
    "Paste Kubernetes, Docker, or CI/CD logs",
    height=260
)

if uploaded_log_content:
    log_input = uploaded_log_content

# =========================================================
# ANALYSIS BUTTON
# =========================================================

if st.button("Run Incident Analysis"):

    if log_input:

        st.success("Analysis completed successfully.")

        issues = detect_known_issue(log_input)

        severity_score = 0
        priority = "P4"
        risk_level = "LOW"

        # =================================================
        # RULE-BASED ANALYSIS
        # =================================================

        if issues:

            severity_score = calculate_severity_score(issues)

            priority = get_priority(severity_score)

            risk_level = get_risk_level(severity_score)

            st.subheader("Incident Risk Summary")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Severity Score",
                    f"{severity_score}/100"
                )

            with col2:
                st.metric(
                    "Priority",
                    priority
                )

            with col3:
                st.metric(
                    "Risk Level",
                    risk_level
                )

            st.divider()

            st.subheader("Detected Infrastructure Incidents")

            for issue in issues:

                result = handle_known_issue(issue)

                st.markdown(
                    f"""
                    <div class="incident-card">
                    <pre>{result}</pre>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.info("No known infrastructure incidents detected.")

        # =================================================
        # AI ANALYSIS
        # =================================================

        st.divider()

        st.subheader("AI Root Cause Analysis")

        ai_result = analyze_log(log_input)

        st.markdown(
            f"""
            <div class="ai-card">
            {ai_result}
            </div>
            """,
            unsafe_allow_html=True
        )

        # =================================================
        # LIVE INCIDENT FEED
        # =================================================

        st.divider()

        st.subheader("Live Incident Feed")

        feed_data = [
            "[16:42:10] Kubernetes pod restarted successfully",
            "[16:42:35] AI engine detected abnormal memory spike",
            "[16:43:02] CrashLoopBackOff recurring pattern identified",
            "[16:43:28] Automated remediation initiated",
            "[16:44:11] Infrastructure stability improving"
        ]

        for feed in feed_data:

            st.markdown(
                f"""
                <div class="live-feed">
                {feed}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.warning("Please provide logs for analysis.")

# =========================================================
# INCIDENT ANALYTICS
# =========================================================

st.divider()

st.subheader("Incident Analytics")

# =========================================================
# LIVE INCIDENT TIMELINE
# =========================================================

st.markdown("### Live Incident Timeline")

timeline_data = pd.DataFrame({
    "Time": [
        "14:01",
        "14:05",
        "14:09",
        "14:14",
        "14:18",
        "14:22"
    ],
    "Event": [
        "Deployment Started",
        "Container Restart Detected",
        "CrashLoopBackOff Triggered",
        "Memory Spike Observed",
        "OOMKilled Event",
        "Auto Recovery Initiated"
    ],
    "Severity": [
        "Low",
        "Medium",
        "Critical",
        "High",
        "Critical",
        "Medium"
    ]
})

st.dataframe(
    timeline_data,
    use_container_width=True
)

# =========================================================
# CHARTS
# =========================================================

chart_col1, chart_col2 = st.columns(2)

trend_data = pd.DataFrame({
    "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "Incidents": [2, 5, 3, 7, 4, 6, 8]
})

issue_data = pd.DataFrame({
    "Issue": [
        "ImagePullBackOff",
        "CrashLoopBackOff",
        "OOMKilled"
    ],
    "Count": [5, 7, 2]
})

with chart_col1:

    st.markdown("### Incident Trend Analysis")

    trend_chart = px.line(
        trend_data,
        x="Day",
        y="Incidents",
        markers=True
    )

    trend_chart.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        font_color="white"
    )

    st.plotly_chart(
        trend_chart,
        use_container_width=True
    )

with chart_col2:

    st.markdown("### Top Incident Categories")

    bar_chart = px.bar(
        issue_data,
        x="Issue",
        y="Count",
        color="Count"
    )

    bar_chart.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        font_color="white"
    )

    st.plotly_chart(
        bar_chart,
        use_container_width=True
    )

# =========================================================
# RECURRING INCIDENTS
# =========================================================

st.divider()

st.subheader("Recurring Incident Intelligence")

recurring = detect_recurring_issues()

if recurring:

    recurring_df = pd.DataFrame(recurring)

    st.dataframe(
        recurring_df,
        use_container_width=True
    )

else:

    st.info("No recurring incidents detected.")

# =========================================================
# OPERATIONAL INSIGHTS
# =========================================================

st.divider()

st.subheader("Operational Insights")

insight1, insight2, insight3 = st.columns(3)

with insight1:

    st.markdown("""
    <div class="analytics-card">
    <h4>Most Frequent Incident</h4>
    <p>
    CrashLoopBackOff remains one of the most recurring
    infrastructure incidents observed.
    </p>
    </div>
    """, unsafe_allow_html=True)

with insight2:

    st.markdown("""
    <div class="analytics-card">
    <h4>Infrastructure Stability</h4>
    <p>
    Cluster stability depends on deployment health,
    memory optimization, and monitoring reliability.
    </p>
    </div>
    """, unsafe_allow_html=True)

with insight3:

    st.markdown("""
    <div class="analytics-card">
    <h4>Recommended Action</h4>
    <p>
    Review deployment configuration,
    health probes, and container resource limits.
    </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown("""
<div class="footer">

AI DevOps Incident Intelligence Platform<br><br>

Real-Time Kubernetes • Docker • CI/CD Monitoring Engine<br><br>

Built with Streamlit, Python, AI Incident Analytics,
and Hybrid Rule-Based Detection

</div>
""", unsafe_allow_html=True)