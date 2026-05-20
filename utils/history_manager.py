import json
import os
from datetime import datetime
from collections import Counter


HISTORY_FILE = "data/incident_history.json"


# =========================================
# CREATE DATA DIRECTORY + FILE
# =========================================
def initialize_history():

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(HISTORY_FILE):

        with open(HISTORY_FILE, "w") as f:

            json.dump([], f, indent=4)


# =========================================
# LOAD HISTORY
# =========================================
def load_history():

    initialize_history()

    try:

        with open(HISTORY_FILE, "r") as f:

            return json.load(f)

    except Exception:

        return []


# =========================================
# SAVE INCIDENT
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
# TOTAL INCIDENTS
# =========================================
def get_incident_count():

    history = load_history()

    return len(history)


# =========================================
# CRITICAL INCIDENT COUNT
# =========================================
def get_critical_count():

    history = load_history()

    count = 0

    for incident in history:

        if incident.get("severity") == "HIGH":

            count += 1

    return count


# =========================================
# RECURRING INCIDENTS
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

        if count >= 2:

            recurring.append({
                "issue": issue,
                "count": count
            })

    return recurring


# =========================================
# INCIDENT TREND DATA
# =========================================
def get_incident_trend():

    history = load_history()

    trend = {}

    for incident in history:

        date = incident["timestamp"].split(" ")[0]

        trend[date] = trend.get(date, 0) + 1

    return trend


# =========================================
# ISSUE DISTRIBUTION
# =========================================
def get_issue_distribution():

    history = load_history()

    counter = Counter()

    for incident in history:

        issues = incident.get("issues", [])

        for issue in issues:

            counter[issue] += 1

    return dict(counter)