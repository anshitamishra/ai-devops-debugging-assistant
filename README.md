# AI DevOps Debugging Assistant

This project is an AI-powered and rule-based DevOps debugging assistant with agentic capabilities. It helps in identifying and resolving issues from Kubernetes and CI/CD pipelines.

The goal of this project is to reduce the time spent manually analyzing logs by providing clear root causes, fixes, and actionable next steps.

---

## Features

- Detects common issues like:
  - ImagePullBackOff
  - CrashLoopBackOff
  - OOMKilled
  - Permission errors

- Uses rule-based logic for instant detection of known issues  
- Uses AI to analyze unknown or complex logs  
- Provides structured output with:
  - Severity
  - Root Cause
  - Fix
  - Suggested Action
  - Next Step (agentic behavior)

- Fetches logs directly from Kubernetes pods  
- Falls back to `kubectl describe` when logs are not available  
- Fetches Jenkins build logs using API  

- Supports CLI usage:
  - `--log`
  - `--file`
  - `--pod`
  - `--jenkins`

- Simple UI using Streamlit  

---

## Tech Stack

- Python  
- Kubernetes (kubectl)  
- Jenkins API  
- Streamlit  
- LLM for analysis  

---
## How to Run

### CLI

```bash
python main.py --log "CrashLoopBackOff error"
python main.py --file logs.txt
python main.py --pod <pod-name>
python main.py --jenkins --job <job-name>
```
### UI

```bash
streamlit run app.py
```
Then open:
http://localhost:8501


---
## How it Works

The system follows a hybrid approach:
1. It first checks logs using rule-based   detection for known issues
2. If a match is found, it instantly returns a structured response
3. If the issue is unknown, logs are sent to an AI model for analysis

For Kubernetes:

- It tries kubectl logs
- If logs are not available, it uses kubectl describe to get detailed events

The output is structured to not only identify the issue but also guide the next steps, making it more like a decision-support DevOps assistant.

## What I Learned
 - End-to-end CI/CD workflow using Jenkins, Docker, and Kubernetes
 - Kubernetes debugging using logs and describe
 - Running system commands using Python  (subprocess)
 - Integrating APIs and AI models
 - Designing hybrid systems using rule-based and AI approaches

## Future Improvements
- Auto-remediation (e.g., restarting pods automatically)
- Integration with monitoring tools (Prometheus, Grafana)
- Real-time alerts (Slack/Email)
- More advanced UI dashboard

## Author
Built as part of hands-on learning in DevOps, Cloud, and AI.


---
