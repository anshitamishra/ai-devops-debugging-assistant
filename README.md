# AI DevOps Debugging Assistant

This project is a simple DevOps tool that helps in debugging issues from Kubernetes and CI/CD pipelines using a mix of rule-based logic and AI.

The idea behind this project is to reduce the time spent in manually reading logs and figuring out what went wrong.

---

## Features

- Detects common issues like:
  - ImagePullBackOff
  - CrashLoopBackOff
  - OOMKilled
  - Permission errors

- Uses AI to analyze unknown or complex logs  
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
The system first checks if the issue is a known one using simple rules.
If it matches, it directly gives the root cause and fix.
If the issue is not recognized, the logs are passed to an AI model which analyzes them and suggests possible fixes.

For Kubernetes:
It tries kubectl logs
If logs are not available, it uses kubectl describe to get more details

## What I Learned
How Kubernetes debugging actually works
How to use subprocess to run system commands
How to integrate APIs (Jenkins)
How to design a system using both rule-based and AI approaches

## Future Improvements
Auto-fix issues (like restarting pods)
Add alerts (Slack/Email)
Better UI dashboard

## Author
Built as part of hands-on learning in DevOps, Cloud, and AI.


---
