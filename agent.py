import subprocess
import requests
import re

API_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"


def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()


def handle_special_commands(user_input):
    user_input = user_input.lower()

    # Restart app
    if "restart" in user_input:
        return "kubectl rollout restart deployment devops-app"

    # Scale app
    if "scale" in user_input:
        match = re.search(r'\d+', user_input)
        if match:
            replicas = match.group()
            return f"kubectl scale deployment devops-app --replicas={replicas}"
        else:
            return "UNKNOWN"

    # Get all resources
    if "get all" in user_input or "all resources" in user_input:
        return "kubectl get all"

    # Describe pod
    if "describe pod" in user_input:
        parts = user_input.split()
        if len(parts) >= 3:
            pod_name = parts[-1]
            return f"kubectl describe pod {pod_name}"
        else:
            return "UNKNOWN"

    return None


def get_ai_command(user_input):
    prompt = f"""
You are a DevOps assistant.

Convert user request into kubectl command.

Supported operations:
- Get pods
- Get logs
- Describe resources
- Restart deployment
- Scale deployment
- Get services
- Get ingress
- Get nodes
- Get all resources
- Rollback deployment
- Namespace-specific queries

Rules:
- Use labels when possible
- Use namespace if mentioned
- Only return command
- No explanation
- If unclear return UNKNOWN

User Request:
{user_input}
"""

    try:
        response = requests.post(API_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        })

        result = response.json()
        command = result.get("response") or result.get("message", {}).get("content")
        return command.strip()

    except Exception as e:
        return "ERROR"


def agent():
    print("=== AI DevOps Agent ===")
    print("Type 'exit' to stop\n")

    while True:
        user_input = input("Ask anything: ")

        if user_input.lower() == "exit":
            break

        # First check rule-based commands
        command = handle_special_commands(user_input)

        #  If not matched, use AI
        if not command:
            command = get_ai_command(user_input)

        print("\nGenerated Command:", command)

        if command == "UNKNOWN" or command == "ERROR":
            print("Could not understand request\n")
            continue

        if command.startswith("kubectl"):
         output = run_command(command)
        else:
         output = "Blocked unsafe command"

        print("\n========== OUTPUT ==========\n")
        print(output)
        print("\n-----------------------------\n")


if __name__ == "__main__":
    agent()