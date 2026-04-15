import argparse
from utils.detector import detect_known_issue, handle_known_issue
from ai_engine.analyzer import analyze_log
from k8s.fetcher import get_pod_logs


def run_analysis(log_data):
    print("\n=== AI DevOps Debugging Assistant ===\n")

    # ---------------- RULE-BASED FIRST ----------------
    issues = detect_known_issue(log_data)

    if issues:
        print("========== RULE-BASED ANALYSIS ==========\n")
        for issue in issues:
            print(handle_known_issue(issue))
        return

    # ---------------- AI ANALYSIS ----------------
    print("========== AI ANALYSIS ==========\n")

    ai_output = analyze_log(log_data)

    if ai_output and "⚠️" not in ai_output:
        print(ai_output.strip())
        return

    # ---------------- FALLBACK ----------------
    print("⚠️ AI failed or unavailable. Falling back to rule-based detection...\n")

    fallback_issues = detect_known_issue(log_data)

    if fallback_issues:
        print("========== FALLBACK ANALYSIS ==========\n")
        for issue in fallback_issues:
            print(handle_known_issue(issue))
    else:
        print("No issues detected.")


# ---------------- FILE INPUT ----------------
def process_file(file_path):
    try:
        with open(file_path, "r") as f:
            logs = f.read()   # ✅ FULL LOG, not line-by-line
            run_analysis(logs)

    except FileNotFoundError:
        print("File not found. Please check path.")


# ---------------- K8S LOGS ----------------
def process_k8s_logs(logs):
    if not logs:
        print("No logs found or pod may not exist")
        return

    print("\n========== LOG PREVIEW ==========\n")

    log_lines = logs.split("\n")

    # Show last few lines only (clean preview)
    preview = "\n".join(log_lines[-10:])
    print(preview)

    print("\n----------------------------------\n")

    # 🔥 PASS FULL LOG (IMPORTANT FIX)
    run_analysis(logs)


# ---------------- MAIN ----------------
def main():
    parser = argparse.ArgumentParser(description="AI DevOps Debugging Assistant")

    parser.add_argument("--log", type=str, help="Single log input")
    parser.add_argument("--file", type=str, help="Path to log file")
    parser.add_argument("--pod", type=str, help="Fetch logs from Kubernetes pod")

    args = parser.parse_args()

    if args.log:
        run_analysis(args.log)

    elif args.file:
        process_file(args.file)

    elif args.pod:
        logs = get_pod_logs(args.pod)
        process_k8s_logs(logs)

    else:
        logs = input("Enter logs: ")
        run_analysis(logs)


if __name__ == "__main__":
    main()