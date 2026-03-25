# AI DevOps Debugging Assistant

An AI-powered DevOps tool that automates debugging of Kubernetes pods and CI/CD pipelines.

## Features

- Rule-based detection for common issues:
  - ImagePullBackOff
  - CrashLoopBackOff
  - OOMKilled
  - Permission errors

- AI-based analysis for unknown issues
- Kubernetes integration (kubectl logs + describe fallback)
- Jenkins integration using REST API
- CLI support:
  - --log
  - --file
  - --pod
  - --jenkins
- Streamlit UI for easy usage

## Tech Stack

- Python
- Kubernetes
- Jenkins
- Streamlit
- AI (LLM)

## Usage

### CLI
```bash
python main.py --log "CrashLoopBackOff error"
python main.py --file logs.txt
python main.py --pod <pod-name>
