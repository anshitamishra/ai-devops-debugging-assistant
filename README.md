# AI DevOps Incident Intelligence Platform

Enterprise-grade AI-powered infrastructure incident monitoring and operational intelligence platform for Kubernetes and CI/CD environments.

---

## Features

- AI Root Cause Analysis
- Kubernetes Incident Detection
- Severity & Risk Analytics
- Live Incident Feed
- Recurring Incident Intelligence
- Operational Monitoring Dashboard
- Infrastructure Stability Insights
- Hybrid AI + Rule-Based Detection
- Automated Incident Recommendations

---

## Supported Incident Types

- CrashLoopBackOff
- OOMKilled
- ImagePullBackOff
- Container Restart Failures
- Metrics Server Failures
- Kubernetes Resource Issues

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend Logic |
| Streamlit | Dashboard UI |
| Plotly | Interactive Analytics |
| Pandas | Data Processing |
| JSON | Incident History Storage |
| AI Analysis Engine | Root Cause Analysis |

---

## Dashboard Preview

### Main Dashboard

![Dashboard](assets/dashboard.png)

---

### AI Root Cause Analysis

![Analysis](assets/analysis.png)

---

### Incident Analytics

![Analytics](assets/analytics.png)

---

### Live Incident Feed

![Feed](assets/feed.png)

---

## Project Architecture

```text
app.py
│
├── ai_engine/
│   └── analyzer.py
│
├── utils/
│   ├── detector.py
│   ├── severity_engine.py
│   └── history_manager.py
│
├── data/
│   └── incident_history.json
│
└── assets/
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Example Incident Log

```text
CrashLoopBackOff error because application failed to connect to MongoDB database and OOMKilled detected
```

---

## AI Operational Insights

The platform provides:

- AI-generated root cause analysis
- Kubernetes remediation recommendations
- Severity prioritization
- Infrastructure trend analytics
- Operational intelligence reporting

---

## Future Improvements

- Real-time Kubernetes cluster integration
- Prometheus/Grafana monitoring
- LLM-powered anomaly detection
- Slack/MS Teams alert integration
- Auto-remediation workflows

---

## Author

Anshita Mishra