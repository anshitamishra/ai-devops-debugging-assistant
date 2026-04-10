import requests

API_URL = "http://host.docker.internal:11434"
MODEL = "gemma3:4b"


def analyze_log(log):
    prompt = f"""
You are a senior DevOps engineer with expertise in Kubernetes, Jenkins, and CI/CD systems.

Analyze the given logs and respond ONLY in the following format:

Severity:
<LOW | MEDIUM | HIGH>

Root Cause:
<one clear and specific reason>

Fix:
1. step
2. step

Suggested Action:
<exact kubectl / Jenkins / command>

Next Step:
<what user should do next>

STRICT RULES:
- Do NOT explain outside format
- If Kubernetes issue → include kubectl commands
- If CI/CD issue → include Jenkins fixes
- Avoid generic answers
- Be precise and actionable

Logs:
{log}
"""

    try:
        response = requests.post(
            API_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=10
        )

        if response.status_code != 200:
            return "⚠️ AI service returned an error"

        try:
            result = response.json()
        except:
            return "⚠️ Invalid JSON response from AI service"

        output = result.get("response") or result.get("message", {}).get("content")

        # Validate output format
        if not output or "Severity:" not in output:
            return "⚠️ AI response invalid or incomplete"

        return output.strip()

    except requests.exceptions.Timeout:
        return "⚠️ AI service timeout. Try again."

    except Exception as e:
        return f"⚠️ Error connecting to AI service: {str(e)}"