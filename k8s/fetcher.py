import subprocess


def run_kubectl_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"Exception occurred: {str(e)}"


def get_pod_logs(pod_name, namespace="default"):
    try:
        print(f"\n🔍 Fetching logs for pod: {pod_name} (namespace: {namespace})\n")

        # Step 1: Get logs
        logs = run_kubectl_command(
            ["kubectl", "logs", pod_name, "-n", namespace]
        )

        # Step 2: Get describe output
        describe = run_kubectl_command(
            ["kubectl", "describe", "pod", pod_name, "-n", namespace]
        )

        # Step 3: Get events
        events = run_kubectl_command(
            ["kubectl", "get", "events", "-n", namespace, "--sort-by=.lastTimestamp"]
        )

        # Combine everything
        combined_output = f"""
========== POD LOGS ==========
{logs}

========== POD DESCRIPTION ==========
{describe}

========== CLUSTER EVENTS ==========
{events}
"""

        return combined_output

    except Exception as e:
        return f"Exception occurred: {str(e)}"