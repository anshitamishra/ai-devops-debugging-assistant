import argparse
import os
from datetime import datetime

from utils.detector import detect_known_issue, handle_known_issue
from ai_engine.analyzer import analyze_log
from k8s.fetcher import get_pod_logs

from utils.history_manager import (
    save_incident,
    detect_recurring_issues
)

from utils.severity_engine import (
    calculate_severity_score,
    get_priority,
    get_risk_level
)

from utils.incident_memory import (
    store_incident,
    search_similar_incidents
)


# =========================================
# GENERATE INCIDENT ID
# =========================================
def generate_incident_id():

    return f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}"


# =========================================
# SAVE INCIDENT REPORT
# =========================================
def save_incident_report(incident_id, content):

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

    severity_score = 0
    priority = "P4"
    risk_level = "LOW"

    if issues:

        detected = True

        severity_score = calculate_severity_score(issues)

        priority = get_priority(severity_score)

        risk_level = get_risk_level(severity_score)

        print(f"Incident Risk Level : {risk_level}")
        print(f"Incident Priority   : {priority}")
        print(f"Severity Score      : {severity_score}/100\n")

        report_content += f"Incident Risk Level : {risk_level}\n"
        report_content += f"Incident Priority   : {priority}\n"
        report_content += f"Severity Score      : {severity_score}/100\n\n"

        for issue in issues:

            result = handle_known_issue(issue)

            # =====================================
            # STORE INCIDENT INTO MEMORY
            # =====================================

            store_incident(
                issue=issue,
                root_cause="Detected automatically",
                fix="Generated remediation steps"
            )

            # =====================================
            # SEARCH PREVIOUS INCIDENTS
            # =====================================

            previous = search_similar_incidents(issue)

            if len(previous) > 1:

                print(
                    f"\n[AI MEMORY] Found "
                    f"{len(previous)-1} previous incidents "
                    f"similar to {issue}\n"
                )

                report_content += (
                    f"\n[AI MEMORY] Found "
                    f"{len(previous)-1} previous incidents "
                    f"similar to {issue}\n"
                )

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
    # SAVE INCIDENT HISTORY
    # =====================================

    if detected:

        severity = risk_level

        if issues:

            save_incident(
                incident_id=incident_id,
                severity=severity,
                issues=issues,
                source="Kubernetes/CLI"
            )

    # =====================================
    # EXPORT INCIDENT REPORT
    # =====================================

    save_incident_report(incident_id, report_content)

    # =====================================
    # RECURRING INCIDENT DETECTION
    # =====================================

    recurring = detect_recurring_issues()

    if recurring:

        print("\n========== RECURRING INCIDENTS ==========\n")

        for item in recurring:

            print(
                f"[WARNING] {item['issue']} occurred "
                f"{item['count']} times."
            )


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