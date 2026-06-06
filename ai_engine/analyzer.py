import requests
from datetime import datetime

# =========================================
# OLLAMA CONFIG
# =========================================

API_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"


# =========================================
# MAIN AI ANALYZER
# =========================================

def analyze_log(log):

    # =====================================
    # LOG PREPROCESSING
    # =====================================

    log = log.strip()

    if not log:
        return "⚠️ Empty logs received."

    # =====================================
    # SMART SHORT-LOG DETECTION
    # =====================================

    short_log_mode = False

    if len(log) < 80:
        short_log_mode = True

    # =====================================
    # INCIDENT TIMESTAMP
    # =====================================

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # =====================================
    # AI PROMPT
    # =====================================

    prompt = f"""
You are an elite Senior DevOps Site Reliability Engineer (SRE).

Your task is to analyze Kubernetes, Docker, Jenkins, CI/CD and infrastructure logs.

You MUST return output STRICTLY in the following format.

DO NOT explain outside format.

========================================
AI DEVOPS INCIDENT REPORT
========================================

Timestamp:
{timestamp}

Platform:
<Kubernetes / Jenkins / Docker / CI-CD>

Severity:
<LOW / MEDIUM / HIGH / CRITICAL>

Confidence Score:
<0-100%>

Incident Summary:
<short technical summary>

Root Cause:
<clear exact root cause>

Fix:
1. step
2. step
3. step

Suggested Action:
<exact kubectl / docker / Jenkins command>

Next Step:
<next action engineer should take>

Analysis Mode:
<AI Analysis>

IMPORTANT RULES:
- Be concise
- Be technical
- Always provide commands
- Focus on DevOps troubleshooting
- Mention Kubernetes fixes if relevant
- Mention Jenkins fixes if relevant
- Mention Docker fixes if relevant
- Avoid generic answers

Logs:
{log}
"""

    # =====================================
    # SMALL LOG FALLBACK
    # =====================================

    if short_log_mode:

        return f"""
========================================
AI DEVOPS INCIDENT REPORT
========================================

Timestamp:
{timestamp}

Platform:
Kubernetes

Severity:
LOW

Confidence Score:
65%

Incident Summary:
Log input too small for deep AI analysis.

Root Cause:
Insufficient log data provided.

Fix:
1. Provide complete logs
2. Include deployment/container errors
3. Retry with larger logs

Suggested Action:
kubectl logs <pod-name>

Next Step:
Retry analysis using full logs.

Analysis Mode:
Rule-based fallback triggered
"""

    # =====================================
    # AI REQUEST
    # =====================================

    try:

        print("\n[INFO] Connecting to Ollama AI engine...\n")

        response = requests.post(
            API_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        # =================================
        # RESPONSE STATUS CHECK
        # =================================

        if response.status_code != 200:

            return f"""
⚠️ AI service unavailable.

Status Code:
{response.status_code}

Fallback triggered.
"""

        # =================================
        # JSON PARSE
        # =================================

        result = response.json()

        print("\n[DEBUG] AI API RESPONSE RECEIVED\n")

        # =================================
        # OUTPUT EXTRACTION
        # =================================

        output = result.get("response", "").strip()

        # =================================
        # EMPTY OUTPUT CHECK
        # =================================

        if not output:

            return """
⚠️ AI returned empty response.

Fallback triggered.
"""

        # =================================
        # DEBUG PREVIEW
        # =================================

        print("\n[DEBUG] RESPONSE PREVIEW:\n")
        print(output[:300])

        # =================================
        # SUCCESS
        # =================================

        return f"""
{output}
"""

    # =====================================
    # TIMEOUT ERROR
    # =====================================

    except requests.exceptions.Timeout:

        return """
⚠️ AI request timeout.

Possible Causes:
- Large model loading
- System RAM overload
- Ollama cold start

Suggested Fix:
1. Run:
   ollama run gemma3:4b

2. Retry analysis

3. Increase timeout if needed
"""

    # =====================================
    # CONNECTION ERROR
    # =====================================

    except requests.exceptions.ConnectionError:

        return """
⚠️ Cannot connect to Ollama AI service.

Verify:
1. Ollama installed
2. Ollama running
3. Model downloaded

Commands:
- ollama list
- ollama run gemma3:4b
"""

    # =====================================
    # UNKNOWN ERROR
    # =====================================

    except Exception as e:

        return f"""
⚠️ AI analysis failed.

Error:
{str(e)}
"""