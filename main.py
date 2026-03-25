import argparse
from utils.detector import detect_known_issue, handle_known_issue
from ai_engine.analyzer import analyze_log
from k8s.fetcher import get_pod_logs


def process_logs(logs):
    for log in logs:
        log = log.strip()
        print(f"\nProcessing: {log}")

        issue = detect_known_issue(log)

        if issue:
            print("\n========== RULE-BASED ANALYSIS ==========\n")
            print(handle_known_issue(issue))
        else:
            print("\n========== AI ANALYSIS ==========\n")
            output = analyze_log(log)

            if output:
                print(output.strip())
            else:
                print("No response from AI")

        print("\n-----------------------------\n")


def main():
    parser = argparse.ArgumentParser(description="AI DevOps Debugging Assistant")

    parser.add_argument("--log", type=str, help="Single log input")
    parser.add_argument("--file", type=str, help="Path to log file")
    parser.add_argument("--pod", type=str, help="Fetch logs from Kubernetes pod")

    args = parser.parse_args()

    print("=== AI DevOps Debugging Assistant ===")

    # Case 1: Single log
    if args.log:
        process_logs([args.log])

    # Case 2: File input
    elif args.file:
        try:
            with open(args.file, "r") as f:
                logs = f.readlines()
                process_logs(logs)
        except FileNotFoundError:
            print("File not found. Please check path.")

    # Case 3: Kubernetes pod logs
    elif args.pod:
        logs = get_pod_logs(args.pod)

        # Show small preview (clean output)
        print("\n========== RAW POD DATA (PREVIEW) ==========\n")
        print(logs[:500])  # show first 500 characters only

        # Detect known issue from logs/describe output
        issue = detect_known_issue(logs)

        if issue:
            print("\n========== RULE-BASED ANALYSIS ==========\n")
            print(handle_known_issue(issue))
        else:
            print("\n========== AI ANALYSIS ==========\n")
            output = analyze_log(logs)

            if output:
                print(output.strip())
            else:
                print("No response from AI")

    # Case 4: fallback (manual input)
    else:
        logs = input("Enter logs (comma separated): ")
        log_list = logs.split(",")
        process_logs(log_list)


if __name__ == "__main__":
    main()