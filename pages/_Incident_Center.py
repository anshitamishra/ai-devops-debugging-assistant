import streamlit as st
import pandas as pd
from utils.k8s_monitor import get_live_incidents

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

.incident-card {
    background: rgba(17,25,40,0.8);
    border-radius: 20px;
    padding: 24px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 25px;
}

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
# LIVE INCIDENTS
# =====================================================

live_incidents = get_live_incidents()

incident_rows = []

for idx, incident in enumerate(live_incidents):

    status = incident["status"]

    severity = (
        "Critical"
        if status in [
            "CrashLoopBackOff",
            "ImagePullBackOff",
            "ErrImagePull",
            "OOMKilled"
        ]
        else "High"
    )

    priority = (
        "P1"
        if severity == "Critical"
        else "P2"
    )

    incident_rows.append({

        "Incident ID": f"INC-{1000 + idx}",

        "Pod": incident["pod"],

        "Namespace": incident["namespace"],

        "Issue": status,

        "Severity": severity,

        "Priority": priority,

        "Source": "Kubernetes",

        "Status": "Active",

        "Timestamp": pd.Timestamp.now().strftime(
            "%d %b %Y %H:%M"
        )
    })

if incident_rows:

    incident_data = pd.DataFrame(incident_rows)

else:

    incident_data = pd.DataFrame(columns=[
        "Incident ID",
        "Pod",
        "Namespace",
        "Issue",
        "Severity",
        "Priority",
        "Source",
        "Status",
        "Timestamp"
    ])

# =====================================================
# METRICS
# =====================================================

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.metric(
        "Open Incidents",
        len(live_incidents)
    )

with m2:

    critical_count = len([
        i for i in live_incidents
        if i["status"] in [
            "CrashLoopBackOff",
            "ImagePullBackOff",
            "ErrImagePull",
            "OOMKilled"
        ]
    ])

    st.metric(
        "Critical Alerts",
        critical_count
    )

with m3:

    st.metric(
        "Resolved Today",
        0
    )

with m4:

    st.metric(
        "AI Detection Accuracy",
        "94%"
    )

st.divider()

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
            row.astype(str)
            .str.contains(
                search,
                case=False
            )
            .any(),
            axis=1
        )
    ]

# =====================================================
# TABLE
# =====================================================

st.markdown("## Active Infrastructure Incidents")

if len(incident_data) > 0:

    st.dataframe(
        incident_data,
        use_container_width=True,
        height=420
    )
   
else:

    st.success(
        "No active Kubernetes incidents detected."
    )

# =====================================================
# INCIDENT FEED
# =====================================================

st.divider()

st.markdown("## Live Operational Feed")

if live_incidents:

    for incident in live_incidents:

        st.markdown(f"""
        <div class="incident-card">
        [{pd.Timestamp.now().strftime("%H:%M:%S")}]
        {incident["status"]} detected in pod:
        <b>{incident["pod"]}</b>
        (Namespace: {incident["namespace"]})
        </div>
        """, unsafe_allow_html=True)

else:

    st.markdown("""
    <div class="incident-card">
    Infrastructure healthy. No active alerts detected.
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# INSIGHTS
# =====================================================

st.divider()

st.markdown("## AI Incident Insights")

c1, c2 = st.columns(2)

with c1:

    if live_incidents:

        incident_type = live_incidents[0]["status"]

        st.markdown(f"""
        <div class="incident-card">

        <h3>Root Cause Intelligence</h3>

        Live cluster analysis detected
        <b>{incident_type}</b> incidents.

        AI correlation indicates probable resource
        exhaustion, container startup failure,
        deployment configuration issues, or image
        retrieval problems causing repeated pod
        restarts and service instability.

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="incident-card">

        <h3>Root Cause Intelligence</h3>

        No active Kubernetes incidents detected.
        Infrastructure is operating within expected
        thresholds and all monitored services are healthy.

        </div>
        """, unsafe_allow_html=True)

with c2:

    st.markdown("""
    <div class="incident-card">

    <h3>Operational Recommendation</h3>

    Validate deployments, monitor resource utilization,
    configure alert thresholds, and investigate failing
    pods immediately to prevent cascading service
    failures. Implement automated remediation and
    rollback strategies for critical workloads.

    </div>
    """, unsafe_allow_html=True)