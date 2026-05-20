import json
import os
from datetime import datetime


HISTORY_FILE = "data/incident_history.json"


# =========================================
# CREATE FILE IF NOT EXISTS
# =========================================
def initialize_history():

    if not os.path.exists(HISTORY_FILE):

        with open(HISTORY_FILE, "w") as f:

            json.dump([], f, indent=4)


# =========================================
# LOAD INCIDENT HISTORY
# =========================================
def load_history():

    initialize_history()

    try:

        with open(HISTORY_FILE, "r") as f:

            return json.load(f)

    except Exception:

        return []


# =========================================
# SAVE INCIDENT TO HISTORY
# =========================================
def save_incident(
    incident_id,
    severity,
    issues,
    source="CLI"
):

    history = load_history()

    incident = {
        "incident_id": incident_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "severity": severity,
        "issues": issues,
        "source": source
    }

    history.append(incident)

    with open(HISTORY_FILE, "w") as f:

        json.dump(history, f, indent=4)


# =========================================
# GET TOTAL INCIDENT COUNT
# =========================================
def get_incident_count():

    history = load_history()

    return len(history)

# =========================================
# DETECT RECURRING INCIDENTS
# =========================================
def detect_recurring_issues():

    history = load_history()

    issue_count = {}

    for incident in history:

        issues = incident.get("issues", [])

        for issue in issues:

            issue_count[issue] = issue_count.get(issue, 0) + 1

    recurring = []

    for issue, count in issue_count.items():

        if count >= 3:

            recurring.append({
                "issue": issue,
                "count": count
            })

    return recurring