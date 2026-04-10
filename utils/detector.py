def detect_known_issue(log):
    log_lower = log.lower()
    issues = []

    # Image issues
    if "imagepullbackoff" in log_lower or "errimagepull" in log_lower:
        issues.append("ImagePullBackOff")

    # Crash issues
    if "crashloopbackoff" in log_lower or "back-off restarting" in log_lower:
        issues.append("CrashLoopBackOff")

    # Memory issues
    if "oomkilled" in log_lower:
        issues.append("OOMKilled")

    # Permission issues
    if "permission denied" in log_lower:
        issues.append("PermissionDenied")

    # Container stuck
    if "containercreating" in log_lower:
        issues.append("ContainerCreating")

    # Remove duplicates
    return list(set(issues)) if issues else None


def handle_known_issue(issue):
    if issue == "ImagePullBackOff":
        return """
⚠️ Issue: ImagePullBackOff
Severity: HIGH

Root Cause:
Container image cannot be pulled.

Fix:
1. Verify image name and tag
2. Check registry access

Suggested Command:
kubectl describe pod <pod-name>
"""

    elif issue == "CrashLoopBackOff":
        return """
⚠️ Issue: CrashLoopBackOff
Severity: HIGH

Root Cause:
Container is crashing repeatedly.

Fix:
1. Check logs
2. Verify configs/env variables

Suggested Command:
kubectl logs <pod-name>
"""

    elif issue == "OOMKilled":
        return """
⚠️ Issue: OOMKilled
Severity: HIGH

Root Cause:
Container exceeded memory limits.

Fix:
1. Increase memory limits
2. Optimize application

Suggested Command:
kubectl describe pod <pod-name>
"""

    elif issue == "PermissionDenied":
        return """
⚠️ Issue: PermissionDenied
Severity: MEDIUM

Root Cause:
Permission issue in system/Jenkins.

Fix:
1. Check credentials
2. Fix RBAC permissions
"""

    elif issue == "ContainerCreating":
        return """
⚠️ Issue: ContainerCreating
Severity: MEDIUM

Root Cause:
Pod stuck while starting.

Fix:
1. Check events
2. Verify volumes/network

Suggested Command:
kubectl describe pod <pod-name>
"""

    return ""