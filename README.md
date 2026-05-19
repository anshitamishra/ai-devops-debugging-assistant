# AI DevOps Debugging Assistant

An intelligent DevOps incident analysis system designed to automate infrastructure troubleshooting across Kubernetes and CI/CD environments.

The project combines rule-based detection with AI-powered log analysis to identify failures, generate remediation suggestions, and reduce manual debugging effort during deployments and production incidents.

---

## Overview

Modern DevOps environments generate large volumes of logs and infrastructure events, making manual debugging time-consuming and inefficient.

This project provides a hybrid debugging engine capable of:

- Detecting known infrastructure failures using deterministic rules
- Performing AI-based root cause analysis for complex incidents
- Generating structured incident reports
- Integrating with Kubernetes, Jenkins, Docker, and monitoring systems
- Assisting engineers with remediation steps and operational insights

---

## Core Features

### Hybrid Incident Detection Engine

- Rule-based infrastructure issue detection
- AI-powered log analysis using locally hosted LLMs
- Intelligent fallback mechanism if AI services are unavailable
- Smart filtering of Kubernetes events before AI processing
- Severity and priority classification
- Business impact analysis
 The system is designed to simulate real-world incident response workflows used in modern cloud-native DevOps environments.

---

### Kubernetes Integration

The assistant interacts directly with Kubernetes clusters and supports:

- `kubectl logs`
- `kubectl describe pod`
- `kubectl get events`

Detected Kubernetes issues include:

- CrashLoopBackOff
- ImagePullBackOff
- OOMKilled
- Failed scheduling
- Metrics server failures
- Permission issues
- Container startup failures

---

### AI-Powered Root Cause Analysis

The system integrates with Ollama-hosted local LLMs for infrastructure analysis.

AI analysis generates:

- Incident summary
- Root cause identification
- Confidence score
- Recommended fixes
- Suggested operational commands
- Next-step remediation guidance

The assistant uses filtered infrastructure events to reduce AI inference overhead and improve response quality.

The hybrid architecture improves reliability by combining deterministic rule-based detection with contextual AI-driven analysis.

---

### Jenkins CI/CD Integration

Integrated with Jenkins pipelines for automated troubleshooting during deployments.

Capabilities include:

- Automatic debugging after deployment failure
- Dynamic pod selection
- Kubernetes event inspection
- AI-assisted deployment diagnostics
- CI/CD incident visibility

---

### Incident Reporting System

The assistant automatically generates structured incident reports containing:

- Incident ID
- Timestamp
- Severity
- Priority
- Root cause
- Suggested fixes
- Business impact
- Auto-remediation suggestions

Reports are exported into:

```bash
incident_reports/
```

## System Architecture
```text
Jenkins Pipeline
       │
       ▼
Kubernetes Deployment
       │
       ▼
Cluster Events & Logs
       │
       ▼
Smart Log Filtering Engine
       │
       ▼
Rule-Based Detection
       │
       ▼
AI Analysis Engine (Ollama + Gemma)
       │
       ▼
Structured Incident Report
```

## Project Structure
```text
ai-devops-debugging-assistant/
│
├── ai_engine/
│   └── analyzer.py
│
├── k8s/
│   └── fetcher.py
│
├── utils/
│   └── detector.py
│
├── incident_reports/
│
├── main.py
├── app.py
├── Jenkinsfile
├── known_errors.json
└── README.md
```

## Technologies Used
- Python
- Kubernetes
- Jenkins
- Docker
- Ollama
- Gemma LLM

## How to Run

### Direct Log Analysis

```bash
python main.py --log "CrashLoopBackOff error because application failed to connect to MongoDB database"
 ```
### Analyze Logs from File

```bash
python main.py --file logs.txt
```

### Analyze Kubernetes Pod Events

```bash
python main.py --pod <pod-name>
```
Example:
```bash
python main.py --pod cv-builder-backend-deployment-9f649654f-17v4t
```

## Example Incident Report 

```text
INCIDENT: ImagePullBackOff

Severity:
CRITICAL

Priority:
P1

Root Cause:
Container image cannot be pulled from registry.

Possible Causes:
- Incorrect image name
- Wrong image tag
- Docker registry authentication failure

Suggested Commands:
kubectl describe pod <pod-name>
docker pull <image-name>

Business Impact:
Application deployment failure
```

## Key Engineering Concepts Implemented

- Hybrid AI + rule-based systems
- Kubernetes troubleshooting workflows
- Infrastructure observability
- CI/CD automation
- Smart log preprocessing
- AI-assisted incident response
- Operational reporting systems
- Local LLM deployment using Ollama

## Future Enhancements

Planned improvements include:

- Automated remediation workflows
- Slack and Email alerting
- Multi-cluster support
- Helm integration
- Web dashboard for incident visualization
- Historical incident analytics
- Vector database for incident memory
- Agentic AI workflow orchestration

## Learning Outcomes

Through this project, I explored:

* Kubernetes operations and debugging
* Jenkins pipeline automation
* Infrastructure monitoring
* AI-assisted DevOps workflows
* Local LLM deployment
* Incident response system design
* Python automation for cloud-native environments

## Author

Developed as part of hands-on exploration in Kubernetes, DevOps automation, CI/CD workflows, and AI-assisted infrastructure troubleshooting.


