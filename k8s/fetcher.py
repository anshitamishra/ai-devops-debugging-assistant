import subprocess


def get_pod_logs(pod_name):
    try:
        result = subprocess.run(
            ["kubectl", "logs", pod_name],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            # Fallback to describe
            describe = subprocess.run(
                ["kubectl", "describe", "pod", pod_name],
                capture_output=True,
                text=True
            )

            if describe.returncode != 0:
                return f"Error fetching pod details: {describe.stderr}"

            return describe.stdout

        return result.stdout

    except Exception as e:
        return f"Exception occurred: {str(e)}"