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
Root Cause:
Container image cannot be pulled.

Fix:
1. Check image name
2. Verify registry access

Commands:
- kubectl describe pod <pod-name>
- docker pull <image-name>
"""

    elif issue == "CrashLoopBackOff":
        return """
Root Cause:
Application inside container is crashing repeatedly.

Fix:
1. Check application logs
2. Fix runtime error

Commands:
- kubectl logs <pod-name>
- kubectl describe pod <pod-name>
"""

    elif issue == "OOMKilled":
        return """
Root Cause:
Container exceeded memory limits.

Fix:
1. Increase memory limits
2. Optimize application memory usage

Commands:
- kubectl describe pod <pod-name>
"""

    elif issue == "PermissionDenied":
        return """
Root Cause:
Permission issue in Jenkins or system.

Fix:
1. Check user permissions
2. Verify credentials

Commands:
- Check Jenkins credentials
- Verify file permissions
"""

    return None