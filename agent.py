import subprocess
import requests

API_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"


def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()


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

        command = get_ai_command(user_input)

        print("\nGenerated Command:", command)

        if command == "UNKNOWN" or command == "ERROR":
            print("Could not understand request\n")
            continue

        output = run_command(command)

        print("\n========== OUTPUT ==========\n")
        print(output)
        print("\n-----------------------------\n")


if __name__ == "__main__":
    agent()