import requests

API_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"




def analyze_log(log):
    prompt = f"""
You are a senior DevOps engineer.

Analyze the logs and respond in this EXACT structured format:

Severity:
<LOW | MEDIUM | HIGH>

Root Cause:
<one clear reason>

Fix:
1. step
2. step

Suggested Action:
<exact command or action>

Next Step:
<what user should do next>

Rules:
- Be specific
- If Kubernetes issue → give kubectl commands
- If Jenkins issue → give pipeline or permission fixes
- Do NOT give generic answers

Logs:
{log}
"""

    try:
        response = requests.post(API_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        })

        result = response.json()
        return result.get("response") or result.get("message", {}).get("content")

    except Exception as e:
        return f"Error connecting to AI service: {str(e)}"