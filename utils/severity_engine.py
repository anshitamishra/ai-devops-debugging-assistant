SEVERITY_MAP = {
    "CrashLoopBackOff": 90,
    "ImagePullBackOff": 85,
    "OOMKilled": 95,
    "MetricsServerIssue": 70,
    "MonitoringFailure": 65,
    "PermissionDenied": 60,
    "ContainerCreating": 50
}


# =========================================
# CALCULATE SEVERITY SCORE
# =========================================
def calculate_severity_score(issues):

    total = 0

    for issue in issues:

        total += SEVERITY_MAP.get(issue, 40)

    return min(total, 100)


# =========================================
# GET PRIORITY
# =========================================
def get_priority(score):

    if score >= 90:
        return "P1"

    elif score >= 75:
        return "P2"

    elif score >= 50:
        return "P3"

    return "P4"


# =========================================
# GET RISK LEVEL
# =========================================
def get_risk_level(score):

    if score >= 90:
        return "CRITICAL"

    elif score >= 75:
        return "HIGH"

    elif score >= 50:
        return "MEDIUM"

    return "LOW"