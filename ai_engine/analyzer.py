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

    # 🧠 OPTIONAL: Skip AI for very small logs
    if len(log.strip()) < 30:
        return "⚠️ Using rule-based analysis (log too small for AI)"

    try:
        response = requests.post(
            API_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=8
        )

        # ❌ AI service failed
        if response.status_code != 200:
            return "⚠️ AI unavailable — fallback to rule-based analysis"

        try:
            result = response.json()
        except Exception:
            return "⚠️ AI returned invalid response — using fallback"

        output = result.get("response") or result.get("message", {}).get("content")

        # ❌ AI output not usable
        if not output or "Severity:" not in output:
            return "⚠️ AI response incomplete — fallback triggered"

        return output.strip()

    # ⏳ Timeout case
    except requests.exceptions.Timeout:
        return "⚠️ AI timeout — fallback to rule-based analysis"

    # 🔌 Connection / any error
    except Exception:
        return "⚠️ AI not reachable — fallback to rule-based analysis"