# AI DevOps Debugging Assistant

An AI-powered DevOps debugging system integrated with Kubernetes and Jenkins to automatically detect, analyze, and resolve infrastructure issues.

This project reduces manual debugging effort by combining rule-based detection with AI-based log analysis.

---

##  Key Features

###  Hybrid Debugging Engine
- Rule-based detection for known issues  
- AI-based analysis for complex/unknown errors  
- Automatic fallback if AI is unavailable  

---

###  Kubernetes Integration
- Fetches logs using:
  - kubectl logs
  - kubectl describe pod
  - kubectl get events

- Detects issues like:
  - CrashLoopBackOff  
  - ImagePullBackOff  
  - OOMKilled  
  - Permission issues  

---

###  AI Log Analysis
- Uses LLM to analyze logs  
- Returns structured output:
  - Severity  
  - Root Cause  
  - Fix  
  - Suggested Action  
  - Next Step  

---

###  Jenkins CI/CD Integration
- Automatically runs debugging after deployment  
- Dynamically selects failing pods  
- Enables automated issue detection in pipeline  

---

##  Architecture

Jenkins Pipeline → Kubernetes Deployment → AI Debugging Assistant

1. Jenkins deploys application to Kubernetes  
2. Pod status is checked  
3. AI assistant fetches logs from failing pods  
4. Issues are analyzed using rule-based + AI logic  

---

##  Project Structure
```
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
├── main.py
├── app.py (optional UI)
└── README.md
```

##  How to Run

### CLI Usage

```bash
python main.py --log "CrashLoopBackOff error"
python main.py --file logs.txt
python main.py --pod <pod-name>
```

---

## How It Works
	-	Logs are fetched from Kubernetes
	-	Rule-based detection runs first
	-	If issue is unknown → sent to AI model
	-	If AI fails → fallback to rule-based detection
	- Outputs structured debugging suggestions

 ## Example output
```
Severity: HIGH
Root Cause: Container is crashing repeatedly

Fix:
- Check logs
- Verify environment variables

Suggested Action:
kubectl logs <pod-name>

Next Step:
Restart deployment after fix
```

## What I Learned
- CI/CD pipeline using Jenkins
-	Kubernetes debugging (logs, events, describe)
-	AI + rule-based hybrid systems
-	Python automation with subprocess
-	System design for DevOps workflows

## Future Improvements
- Helm integration for scalable deployments
-	Auto-remediation (restart pods automatically)
-	Slack/Email alerts
-	Web dashboard for visualization

## Author
Built as part of hands-on DevOps + AI learning
