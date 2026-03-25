import requests

API_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"


def analyze_log(log):
    prompt = f"""
You are a DevOps engineer.

Analyze the logs below and give output in EXACT format:

Root Cause:
<one specific reason only>

Fix:
1. step
2. step

Commands:
- command
- command

Be specific. If it's Kubernetes, give kubectl commands.
If it's Jenkins, give pipeline or permission fixes.

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