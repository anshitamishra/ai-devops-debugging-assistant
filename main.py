import argparse
from utils.detector import detect_known_issue, handle_known_issue
from ai_engine.analyzer import analyze_log
from k8s.fetcher import get_pod_logs


def process_logs(logs):
    for log in logs:
        log = log.strip()

        if not log:
            continue

        print(f"\nProcessing: {log}")

        issues = detect_known_issue(log)

        if issues:
            print("\n========== RULE-BASED ANALYSIS ==========\n")
            for issue in issues:
                print(handle_known_issue(issue))

        else:
            print("\n========== AI ANALYSIS ==========\n")
            output = analyze_log(log)

            if output and "Error connecting" not in output:
                print(output.strip())

            else:
                print("⚠️ AI failed. Falling back to rule-based detection...\n")

                fallback = detect_known_issue(log)

                if fallback:
                    for issue in fallback:
                        print(handle_known_issue(issue))
                else:
                    print("No issues detected.")

        print("\n-----------------------------\n")


def process_k8s_logs(logs):
    if not logs:
        print("No logs found or pod may not exist")
        return

    print("\n========== RAW POD DATA (PREVIEW) ==========\n")

    log_lines = logs.split("\n")

    # Show last 10 lines
    print("\n".join(log_lines[-10:]))

    # Detect all issues
    all_issues = []

    for line in log_lines:
        issues = detect_known_issue(line)
        if issues:
            all_issues.extend(issues)

    all_issues = sorted(list(set(all_issues)))

    if all_issues:
        print("\n========== RULE-BASED ANALYSIS ==========\n")
        for issue in all_issues:
            print(handle_known_issue(issue))

    else:
        print("\n========== AI ANALYSIS ==========\n")
        output = analyze_log(logs)

        if output and "Error connecting" not in output:
            print(output.strip())

        else:
            print("⚠️ AI failed. Falling back to rule-based detection...\n")

            fallback_issues = []

            for line in log_lines:
                detected = detect_known_issue(line)
                if detected:
                    fallback_issues.extend(detected)

            fallback_issues = list(set(fallback_issues))

            if fallback_issues:
                for issue in fallback_issues:
                    print(handle_known_issue(issue))
            else:
                print("No issues detected even in fallback.")


def main():
    parser = argparse.ArgumentParser(description="AI DevOps Debugging Assistant")

    parser.add_argument("--log", type=str, help="Single log input")
    parser.add_argument("--file", type=str, help="Path to log file")
    parser.add_argument("--pod", type=str, help="Fetch logs from Kubernetes pod")

    args = parser.parse_args()

    print("\n=== AI DevOps Debugging Assistant ===\n")

    if args.log:
        process_logs([args.log])

    elif args.file:
        try:
            with open(args.file, "r") as f:
                logs = f.readlines()
                process_logs(logs)
        except FileNotFoundError:
            print("File not found. Please check path.")

    elif args.pod:
        logs = get_pod_logs(args.pod)
        process_k8s_logs(logs)

    else:
        logs = input("Enter logs (comma separated): ")
        log_list = logs.split(",")
        process_logs(log_list)


if __name__ == "__main__":
    main()