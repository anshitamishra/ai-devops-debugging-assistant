from utils.prometheus_monitor import (
    get_cpu_usage,
    get_ram_available,
    get_system_uptime
)


def analyze_with_ai(logs):

    logs = logs.lower()

    # =========================
    # FETCH PROMETHEUS METRICS
    # =========================

    cpu = get_cpu_usage()
    ram = get_ram_available()
    uptime = get_system_uptime()

    print("\n==============================")
    print("      SYSTEM METRICS")
    print("==============================")

    print("\nCPU Usage:")
    print(cpu)

    print("\nRAM Available:")
    print(ram)

    print("\nSystem Uptime:")
    print(uptime)

    analysis = []

    # =========================
    # LOG ANALYSIS
    # =========================

    if "crashloopbackoff" in logs:

        analysis.append("""
### CrashLoopBackOff Analysis

Root cause indicates repeated container startup failure.

Possible reasons:
- Invalid environment variables
- Application startup crash
- Dependency failure
- Port conflicts

Recommended Actions:
1. Validate deployment configuration
2. Check application logs
3. Verify Kubernetes secrets/configmaps
4. Restart deployment after fix

Business Impact:
Critical application downtime risk detected.
""")

    if "imagepullbackoff" in logs:

        analysis.append("""
### ImagePullBackOff Analysis

Container image could not be pulled from registry.

Possible reasons:
- Incorrect image tag
- Registry authentication issue
- Network restrictions

Recommended Actions:
1. Verify image name and tag
2. Validate Docker registry credentials
3. Check cluster internet access

Business Impact:
Deployment pipeline blocked.
""")

    if "memory" in logs or "oomkilled" in logs:

        analysis.append("""
### Memory Utilization Analysis

Abnormal memory consumption pattern detected.

Possible reasons:
- Memory leak
- Inefficient workload allocation
- Resource limit misconfiguration

Recommended Actions:
1. Increase memory limits
2. Optimize application usage
3. Enable autoscaling policies

Business Impact:
Infrastructure instability possible.
""")

    # =========================
    # DEFAULT RESPONSE
    # =========================

    if not analysis:

        return """
### AI Infrastructure Analysis

No major infrastructure anomaly detected.

System Status:
- Kubernetes cluster stable
- No critical deployment failures
- Infrastructure operating normally

Recommendation:
Continue observability monitoring and log collection.
"""

    return "\n".join(analysis)


# =========================
# TEST RUN
# =========================

if __name__ == "__main__":

    sample_logs = """
    pod entered crashloopbackoff state
    """

    result = analyze_with_ai(sample_logs)

    print("\n==============================")
    print("        AI ANALYSIS")
    print("==============================")

    print(result)