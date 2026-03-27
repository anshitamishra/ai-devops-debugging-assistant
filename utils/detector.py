def detect_known_issue(log):
    log_lower = log.lower()

    if "imagepullbackoff" in log_lower:
        return "ImagePullBackOff"
    elif "crashloopbackoff" in log_lower:
        return "CrashLoopBackOff"
    elif "oomkilled" in log_lower:
        return "OOMKilled"
    elif "permission denied" in log_lower:
        return "PermissionDenied"

    return None


def handle_known_issue(issue):
    if issue == "ImagePullBackOff":
        return """
⚠️ Severity: HIGH

Root Cause:
Container image cannot be pulled due to incorrect image name or missing registry access.

Fix:
1. Verify image name and tag
2. Check registry authentication

Suggested Action:
kubectl describe pod <pod-name>

Next Step:
Fix image configuration and redeploy the pod
"""

    elif issue == "CrashLoopBackOff":
        return """
⚠️ Severity: HIGH

Root Cause:
Application inside container is crashing repeatedly.

Fix:
1. Check application logs
2. Fix runtime errors

Suggested Action:
kubectl logs <pod-name>

Next Step:
Debug the application and restart deployment
"""

    elif issue == "OOMKilled":
        return """
⚠️ Severity: HIGH

Root Cause:
Container exceeded memory limits and was terminated.

Fix:
1. Increase memory limits
2. Optimize memory usage

Suggested Action:
kubectl describe pod <pod-name>

Next Step:
Update resource limits and redeploy
"""

    elif issue == "PermissionDenied":
        return """
⚠️ Severity: MEDIUM

Root Cause:
Permission issue in Jenkins or system configuration.

Fix:
1. Verify user permissions
2. Check credentials configuration

Suggested Action:
Check Jenkins credentials and access settings

Next Step:
Update permissions and re-run the pipeline
"""

    return None