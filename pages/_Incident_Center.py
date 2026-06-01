import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Incident Center",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #050816, #0b1220);
    color: white;
}

/* TABLE CARD */

.incident-card {
    background: rgba(17,25,40,0.8);
    border-radius: 20px;
    padding: 24px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 25px;
}

/* BADGES */

.critical {
    background: rgba(239,68,68,0.15);
    color: #ef4444;
    padding: 8px 14px;
    border-radius: 30px;
    font-weight: 700;
}

.high {
    background: rgba(249,115,22,0.15);
    color: #f97316;
    padding: 8px 14px;
    border-radius: 30px;
    font-weight: 700;
}

.medium {
    background: rgba(234,179,8,0.15);
    color: #eab308;
    padding: 8px 14px;
    border-radius: 30px;
    font-weight: 700;
}

.active {
    color: #ef4444;
    font-weight: 700;
}

.monitoring {
    color: #22c55e;
    font-weight: 700;
}

.investigating {
    color: #f97316;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.title("Incident Management Center")

st.markdown("""
Centralized AI-powered infrastructure incident tracking and operational monitoring.
""")

# =====================================================
# METRICS
# =====================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Open Incidents", "12")

with m2:
    st.metric("Critical Alerts", "5")

with m3:
    st.metric("Resolved Today", "8")

with m4:
    st.metric("AI Detection Accuracy", "94%")

st.divider()

# =====================================================
# INCIDENT DATA
# =====================================================

incident_data = pd.DataFrame({
    "Incident ID": [
        "INC-2026-1024",
        "INC-2026-1025",
        "INC-2026-1026",
        "INC-2026-1027",
        "INC-2026-1028"
    ],

    "Issue": [
        "CrashLoopBackOff",
        "OOMKilled",
        "ImagePullBackOff",
        "MetricsServerFailure",
        "ContainerRestart"
    ],

    "Severity": [
        "Critical",
        "High",
        "Critical",
        "Medium",
        "Medium"
    ],

    "Priority": [
        "P1",
        "P2",
        "P1",
        "P3",
        "P3"
    ],

    "Source": [
        "Kubernetes",
        "Kubernetes",
        "Docker",
        "Prometheus",
        "Kubernetes"
    ],

    "Status": [
        "Active",
        "Investigating",
        "Monitoring",
        "Resolved",
        "Monitoring"
    ],

    "Timestamp": [
        "20 May 2026 14:20",
        "20 May 2026 14:18",
        "20 May 2026 14:10",
        "20 May 2026 13:54",
        "20 May 2026 13:40"
    ]
})

# =====================================================
# SEARCH
# =====================================================

search = st.text_input(
    "Search incidents"
)

if search:

    incident_data = incident_data[
        incident_data.apply(
            lambda row:
            row.astype(str).str.contains(
                search,
                case=False
            ).any(),
            axis=1
        )
    ]

# =====================================================
# TABLE
# =====================================================

st.markdown("## Active Infrastructure Incidents")

st.dataframe(
    incident_data,
    use_container_width=True,
    height=420
)

# =====================================================
# INCIDENT FEED
# =====================================================

st.divider()

st.markdown("## Live Operational Feed")

feed = [
    "[14:21:08] AI anomaly detection triggered",
    "[14:21:15] Kubernetes deployment health degraded",
    "[14:21:32] CrashLoopBackOff recurrence identified",
    "[14:22:01] Automated remediation initiated",
    "[14:22:40] Infrastructure stability improving"
]

for item in feed:

    st.markdown(f"""
    <div class="incident-card">
    {item}
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# INSIGHTS
# =====================================================

st.divider()

st.markdown("## AI Incident Insights")

c1, c2 = st.columns(2)

with c1:

    st.markdown("""
    <div class="incident-card">

    <h3>Root Cause Intelligence</h3>

    CrashLoopBackOff incidents are strongly correlated with invalid MongoDB environment configurations and deployment startup failures.

    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown("""
    <div class="incident-card">

    <h3>Operational Recommendation</h3>

    Enable deployment validation checks and automated rollback mechanisms for unstable Kubernetes releases.

    </div>
    """, unsafe_allow_html=True)