# =========================================
# KNOWN ISSUE DETECTOR
# =========================================

def detect_known_issue(log):

    log_lower = log.lower()

    issues = []

    # =====================================
    # IMAGE ISSUES
    # =====================================

    if "imagepullbackoff" in log_lower or "errimagepull" in log_lower:

        issues.append("ImagePullBackOff")

    # =====================================
    # CRASH ISSUES
    # =====================================

    if "crashloopbackoff" in log_lower or "back-off restarting" in log_lower:

        issues.append("CrashLoopBackOff")

    # =====================================
    # MEMORY ISSUES
    # =====================================

    if "oomkilled" in log_lower:

        issues.append("OOMKilled")

    # =====================================
    # PERMISSION ISSUES
    # =====================================

    if "permission denied" in log_lower:

        issues.append("PermissionDenied")

    # =====================================
    # CONTAINER STARTUP ISSUES
    # =====================================

    if "containercreating" in log_lower:

        issues.append("ContainerCreating")

    # =====================================
    # CPU METRIC ISSUES
    # =====================================

    if "failedgetresourcemetric" in log_lower:

        issues.append("MetricsServerIssue")

    # =====================================
    # NODE EXPORTER FAILURE
    # =====================================

    if "node-exporter" in log_lower and "back-off" in log_lower:

        issues.append("MonitoringFailure")

    # =====================================
    # REMOVE DUPLICATES
    # =====================================

    return list(set(issues)) if issues else None


# =========================================
# AUTO REMEDIATION ENGINE
# =========================================

def handle_known_issue(issue):

    # =====================================
    # IMAGE PULL FAILURE
    # =====================================

    if issue == "ImagePullBackOff":

        return """
========================================
INCIDENT: ImagePullBackOff
========================================

Severity:
CRITICAL

Priority:
P1

Root Cause:
Container image cannot be pulled from registry.

Possible Causes:
- Incorrect image name
- Wrong image tag
- Docker registry authentication failure
- Network connectivity issue

Fix:
1. Verify image name and tag
2. Verify Docker registry credentials
3. Check network connectivity

Suggested Commands:
kubectl describe pod <pod-name>
kubectl get events
docker pull <image-name>

Auto-Remediation Suggestion:
- Verify image exists in registry
- Recreate deployment after fix

Business Impact:
Application deployment failure
"""

    # =====================================
    # CRASH LOOP
    # =====================================

    elif issue == "CrashLoopBackOff":

        return """
========================================
INCIDENT: CrashLoopBackOff
========================================

Severity:
CRITICAL

Priority:
P1

Root Cause:
Container is repeatedly crashing during startup.

Possible Causes:
- Application startup failure
- Invalid environment variables
- Database connection failure
- Port conflicts

Fix:
1. Check application logs
2. Verify configs/env variables
3. Validate dependencies

Suggested Commands:
kubectl logs <pod-name>
kubectl describe pod <pod-name>
kubectl rollout restart deployment <deployment-name>

Auto-Remediation Suggestion:
- Restart deployment
- Re-validate environment variables
- Verify database connectivity

Business Impact:
Service downtime possible
"""

    # =====================================
    # MEMORY ISSUES
    # =====================================

    elif issue == "OOMKilled":

        return """
========================================
INCIDENT: OOMKilled
========================================

Severity:
HIGH

Priority:
P2

Root Cause:
Container exceeded allocated memory limits.

Possible Causes:
- Memory leak
- High workload
- Insufficient Kubernetes limits

Fix:
1. Increase memory limits
2. Optimize application memory usage
3. Analyze memory spikes

Suggested Commands:
kubectl top pods
kubectl describe pod <pod-name>
kubectl set resources deployment <deployment-name>

Auto-Remediation Suggestion:
- Scale deployment
- Increase memory requests/limits

Business Impact:
Performance degradation
"""

    # =====================================
    # PERMISSION ISSUES
    # =====================================

    elif issue == "PermissionDenied":

        return """
========================================
INCIDENT: PermissionDenied
========================================

Severity:
MEDIUM

Priority:
P3

Root Cause:
Permission or RBAC restriction encountered.

Possible Causes:
- Kubernetes RBAC issue
- Jenkins credential issue
- File permission issue

Fix:
1. Verify RBAC roles
2. Check Jenkins credentials
3. Validate filesystem permissions

Suggested Commands:
kubectl auth can-i --list
kubectl describe rolebinding
kubectl describe clusterrolebinding

Auto-Remediation Suggestion:
- Reconfigure RBAC permissions
- Rotate credentials if needed

Business Impact:
Restricted system operations
"""

    # =====================================
    # CONTAINER STARTING ISSUE
    # =====================================

    elif issue == "ContainerCreating":

        return """
========================================
INCIDENT: ContainerCreating
========================================

Severity:
MEDIUM

Priority:
P3

Root Cause:
Pod stuck during startup phase.

Possible Causes:
- Volume mount issue
- Network issue
- Pending PVC
- Image pull delay

Fix:
1. Check Kubernetes events
2. Verify persistent volumes
3. Validate networking

Suggested Commands:
kubectl describe pod <pod-name>
kubectl get pvc
kubectl get events

Auto-Remediation Suggestion:
- Restart pod
- Reattach persistent volume

Business Impact:
Deployment delay
"""

    # =====================================
    # METRICS SERVER ISSUE
    # =====================================

    elif issue == "MetricsServerIssue":

        return """
========================================
INCIDENT: MetricsServerIssue
========================================

Severity:
HIGH

Priority:
P2

Root Cause:
Kubernetes metrics API unavailable.

Possible Causes:
- Metrics server not installed
- Metrics server crash
- API aggregation issue

Fix:
1. Verify metrics server installation
2. Restart metrics server
3. Check API service health

Suggested Commands:
kubectl top pods
kubectl get apiservices
kubectl get pods -n kube-system

Auto-Remediation Suggestion:
- Reinstall metrics-server
- Restart metrics components

Business Impact:
HPA autoscaling failure
"""

    # =====================================
    # MONITORING FAILURE
    # =====================================

    elif issue == "MonitoringFailure":

        return """
========================================
INCIDENT: MonitoringFailure
========================================

Severity:
HIGH

Priority:
P2

Root Cause:
Prometheus node-exporter repeatedly crashing.

Possible Causes:
- Node exporter configuration issue
- Port conflict
- Resource exhaustion

Fix:
1. Check exporter logs
2. Verify monitoring configuration
3. Restart monitoring stack

Suggested Commands:
kubectl logs <node-exporter-pod>
kubectl describe pod <node-exporter-pod>
helm list

Auto-Remediation Suggestion:
- Restart monitoring deployment
- Reinstall exporter if needed

Business Impact:
Monitoring visibility reduced
"""

    # =====================================
    # UNKNOWN ISSUE
    # =====================================

    return """
Unknown issue detected.

Further investigation required.
"""