import argparse
import os
from datetime import datetime

from utils.detector import detect_known_issue, handle_known_issue
from ai_engine.analyzer import analyze_log
from k8s.fetcher import get_pod_logs


# =========================================
# GENERATE INCIDENT ID
# =========================================
def generate_incident_id():

    return f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}"


# =========================================
# SAVE INCIDENT REPORT
# =========================================
def save_incident_report(incident_id, content):

    # Create reports directory automatically
    os.makedirs("incident_reports", exist_ok=True)

    filename = f"incident_reports/{incident_id}.txt"

    try:

        with open(filename, "w", encoding="utf-8") as file:

            file.write(content)

        print(f"\n[INFO] Incident report exported successfully.")
        print(f"[INFO] Report Path: {filename}\n")

    except Exception as e:

        print(f"\n❌ Failed to save incident report: {str(e)}\n")


# =========================================
# INCIDENT REPORT HEADER
# =========================================
def print_header(incident_id):

    header = f"""
======================================================================
              AI DEVOPS INCIDENT REPORT
======================================================================
Incident ID   : {incident_id}
Generated At  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Detection Mode: Hybrid (Rule-Based + AI)
Supported Env : Kubernetes | Jenkins | Docker | CI/CD
======================================================================
"""

    print(header)

    return header


# =========================================
# FINAL STATUS
# =========================================
def print_final_status(detected):

    final_output = "\n" + "=" * 70 + "\n"

    if detected:
        final_output += "FINAL STATUS : INCIDENT DETECTED\n"
    else:
        final_output += "FINAL STATUS : NO MAJOR ISSUES DETECTED\n"

    final_output += "=" * 70 + "\n"

    print(final_output)

    return final_output


# =========================================
# MAIN ANALYSIS ENGINE
# =========================================
def run_analysis(log_data):

    incident_id = generate_incident_id()

    report_content = ""

    # =====================================
    # HEADER
    # =====================================

    header = print_header(incident_id)

    report_content += header + "\n"

    detected = False

    # =====================================
    # RULE-BASED ANALYSIS
    # =====================================

    print("========== RULE-BASED ANALYSIS ==========\n")

    report_content += "========== RULE-BASED ANALYSIS ==========\n\n"

    issues = detect_known_issue(log_data)

    if issues:

        detected = True

        for issue in issues:

            result = handle_known_issue(issue)

            print(result)
            print("-" * 60)

            report_content += result + "\n"
            report_content += "-" * 60 + "\n"

    else:

        no_issue = "No known issues detected using rule-based engine.\n"

        print(no_issue)

        report_content += no_issue

    # =====================================
    # AI ANALYSIS
    # =====================================

    print("\n========== AI ANALYSIS ==========\n")

    report_content += "\n========== AI ANALYSIS ==========\n\n"

    ai_output = analyze_log(log_data)

    # =====================================
    # AI SUCCESS
    # =====================================

    if ai_output and "⚠️" not in ai_output:

        detected = True

        print(ai_output)

        report_content += ai_output + "\n"

    # =====================================
    # AI FAILURE
    # =====================================

    else:

        print(ai_output)

        print("\n⚠️ AI service unavailable or fallback triggered.")

        report_content += ai_output + "\n"
        report_content += "\n⚠️ AI service unavailable or fallback triggered.\n"

    # =====================================
    # FINAL STATUS
    # =====================================

    final_status = print_final_status(detected)

    report_content += final_status

    # =====================================
    # EXPORT INCIDENT REPORT
    # =====================================

    save_incident_report(incident_id, report_content)


# =========================================
# FILE INPUT ANALYSIS
# =========================================
def process_file(file_path):

    try:

        print(f"\n[INFO] Reading log file: {file_path}\n")

        with open(file_path, "r") as f:

            logs = f.read()

        run_analysis(logs)

    except FileNotFoundError:

        print("❌ File not found. Please check file path.")

    except Exception as e:

        print(f"❌ Failed to process file: {str(e)}")


# =========================================
# SMART KUBERNETES LOG PROCESSOR
# =========================================
def process_k8s_logs(logs):

    # =====================================
    # EMPTY LOG CHECK
    # =====================================

    if not logs:

        print("❌ No logs found or pod may not exist.")
        return

    # =====================================
    # PREVIEW SECTION
    # =====================================

    print("\n========== KUBERNETES LOG PREVIEW ==========\n")

    log_lines = logs.split("\n")

    preview = "\n".join(log_lines[-15:])

    print(preview)

    print("\n" + "-" * 70 + "\n")

    # =====================================
    # SMART LOG FILTERING
    # =====================================

    important_keywords = [
        "error",
        "failed",
        "backoff",
        "crashloopbackoff",
        "imagepullbackoff",
        "oomkilled",
        "evicted",
        "unhealthy",
        "warning"
    ]

    filtered_lines = []

    for line in log_lines:

        lower = line.lower()

        if any(keyword in lower for keyword in important_keywords):

            filtered_lines.append(line)

    # =====================================
    # KEEP IMPORTANT LOGS ONLY
    # =====================================

    important_logs = "\n".join(filtered_lines[-20:])

    print("[INFO] Critical Kubernetes events filtered successfully.\n")

    print("========== FILTERED CRITICAL EVENTS ==========\n")

    print(important_logs)

    print("\n" + "-" * 70 + "\n")

    # =====================================
    # SEND FILTERED LOGS TO AI
    # =====================================

    print("[INFO] Sending filtered logs to AI engine...\n")

    run_analysis(important_logs)


# =========================================
# MAIN FUNCTION
# =========================================
def main():

    parser = argparse.ArgumentParser(
        description="AI DevOps Debugging Assistant"
    )

    # =====================================
    # DIRECT LOG INPUT
    # =====================================

    parser.add_argument(
        "--log",
        type=str,
        help="Analyze direct log input"
    )

    # =====================================
    # FILE INPUT
    # =====================================

    parser.add_argument(
        "--file",
        type=str,
        help="Analyze logs from file"
    )

    # =====================================
    # POD ANALYSIS
    # =====================================

    parser.add_argument(
        "--pod",
        type=str,
        help="Fetch and analyze Kubernetes pod logs"
    )

    args = parser.parse_args()

    # =====================================
    # DIRECT LOG ANALYSIS
    # =====================================

    if args.log:

        print("\n[INFO] Starting direct log analysis...\n")

        run_analysis(args.log)

    # =====================================
    # FILE ANALYSIS
    # =====================================

    elif args.file:

        process_file(args.file)

    # =====================================
    # POD ANALYSIS
    # =====================================

    elif args.pod:

        print(f"\n[INFO] Fetching logs from Kubernetes pod: {args.pod}\n")

        logs = get_pod_logs(args.pod)

        process_k8s_logs(logs)

    # =====================================
    # MANUAL INPUT
    # =====================================

    else:

        logs = input("Enter logs to analyze:\n\n")

        run_analysis(logs)


# =========================================
# ENTRY POINT
# =========================================
if __name__ == "__main__":
    main()