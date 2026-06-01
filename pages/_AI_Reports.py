import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Reports",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #050816, #0b1220);
    color: white;
}

.report-card {
    background: rgba(17,25,40,0.78);
    border-radius: 24px;
    padding: 28px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 0 24px rgba(0,0,0,0.35);
    margin-bottom: 20px;
}

.big-title {
    font-size: 48px;
    font-weight: 800;
    color: white;
    line-height: 1.1;
}

.sub-text {
    color: #94a3b8;
    font-size: 18px;
    margin-top: 12px;
}

.metric-box {
    background: rgba(17,25,40,0.75);
    padding: 22px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    text-align: center;
}

.metric-number {
    font-size: 40px;
    font-weight: 700;
    color: white;
}

.metric-label {
    color: #94a3b8;
    font-size: 14px;
    margin-top: 8px;
}

.insight-card {
    background: rgba(17,25,40,0.78);
    border-radius: 22px;
    padding: 24px;
    border-left: 4px solid #3b82f6;
    margin-top: 20px;
}

.executive-card {
    background: linear-gradient(135deg, #111827, #1e293b);
    border-radius: 26px;
    padding: 34px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="report-card">

<div class="big-title">
AI Infrastructure Intelligence Reports
</div>

<div class="sub-text">
AI-generated operational reporting, infrastructure analytics,
and root cause intelligence for Kubernetes and CI/CD ecosystems.
</div>

</div>
""", unsafe_allow_html=True)

# =====================================================
# KPI SECTION
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-number">94%</div>
        <div class="metric-label">AI Detection Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-number">128</div>
        <div class="metric-label">Incidents Analyzed</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-number">17m</div>
        <div class="metric-label">Avg RCA Time</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-number">99.2%</div>
        <div class="metric-label">Infrastructure Availability</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# AI GENERATED SUMMARY
# =====================================================

st.markdown("## AI Generated Executive Summary")

st.markdown("""
<div class="executive-card">

### Infrastructure Stability Assessment

The AI operational intelligence engine identified recurring Kubernetes deployment instability patterns associated with CrashLoopBackOff and memory saturation events.

Root cause correlation analysis indicates that deployment configuration inconsistencies and insufficient memory allocation policies remain the dominant contributors to infrastructure degradation.

AI predictive monitoring forecasts elevated operational risk during high deployment traffic windows unless autoscaling and deployment validation policies are enhanced.

### Strategic Recommendations

- Enable automated deployment rollback policies
- Configure horizontal pod autoscaling
- Improve memory threshold alerting
- Implement deployment validation pipelines
- Optimize Kubernetes workload balancing

</div>
""", unsafe_allow_html=True)

# =====================================================
# CHARTS
# =====================================================

left, right = st.columns(2)

with left:

    st.markdown("## Incident Distribution")

    issue_data = pd.DataFrame({
        "Issue": [
            "CrashLoopBackOff",
            "OOMKilled",
            "ImagePullBackOff",
            "NodeFailure",
            "ContainerRestart"
        ],

        "Count": [
            34,
            18,
            12,
            9,
            21
        ]
    })

    fig = px.bar(
        issue_data,
        x="Issue",
        y="Count",
        color="Count"
    )

    fig.update_layout(
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        font_color="white",
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.markdown("## AI Risk Prediction")

    risk_data = pd.DataFrame({
        "Week": [
            "Week 1",
            "Week 2",
            "Week 3",
            "Week 4",
            "Week 5"
        ],

        "Risk Score": [
            32,
            41,
            56,
            63,
            49
        ]
    })

    line = px.line(
        risk_data,
        x="Week",
        y="Risk Score",
        markers=True
    )

    line.update_layout(
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        font_color="white",
        height=420
    )

    st.plotly_chart(
        line,
        use_container_width=True
    )

# =====================================================
# AI INCIDENT ANALYSIS
# =====================================================

st.markdown("## AI Root Cause Intelligence")

incident_df = pd.DataFrame({

    "Incident": [
        "CrashLoopBackOff",
        "OOMKilled",
        "ImagePullBackOff",
        "MetricsServerFailure",
        "ContainerRestart"
    ],

    "Primary Cause": [
        "Deployment startup failure",
        "Memory exhaustion",
        "Registry authentication issue",
        "Monitoring service instability",
        "Application crash loop"
    ],

    "Risk Level": [
        "Critical",
        "High",
        "Critical",
        "Medium",
        "Medium"
    ],

    "AI Recommendation": [
        "Validate deployment configs",
        "Increase memory allocation",
        "Verify registry credentials",
        "Restart monitoring services",
        "Inspect application runtime logs"
    ]
})

st.dataframe(
    incident_df,
    use_container_width=True,
    height=300
)

# =====================================================
# OPERATIONAL INSIGHTS
# =====================================================

st.markdown("## Operational Intelligence Insights")

i1, i2, i3 = st.columns(3)

with i1:

    st.markdown("""
    <div class="insight-card">

    <h3>Infrastructure Pattern</h3>

    AI monitoring identified deployment instability spikes during high CI/CD activity windows.

    </div>
    """, unsafe_allow_html=True)

with i2:

    st.markdown("""
    <div class="insight-card">

    <h3>Predictive Intelligence</h3>

    Kubernetes worker-node-3 is projected to exceed memory thresholds within the next operational cycle.

    </div>
    """, unsafe_allow_html=True)

with i3:

    st.markdown("""
    <div class="insight-card">

    <h3>Automation Opportunity</h3>

    67% of recurring incidents can be automatically remediated using deployment rollback workflows.

    </div>
    """, unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
<center>

AI DevOps Intelligence Platform<br><br>

Enterprise AI Infrastructure Analytics • Kubernetes Monitoring • Incident Intelligence

</center>
""", unsafe_allow_html=True)