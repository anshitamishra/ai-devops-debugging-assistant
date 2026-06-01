import requests

PROMETHEUS_URL = "http://localhost:9090"


def query_prometheus(query):

    try:
        url = f"{PROMETHEUS_URL}/api/v1/query"

        response = requests.get(
            url,
            params={"query": query},
            timeout=10
        )

        return response.json()

    except Exception as e:

        print("Prometheus Error:", e)

        return {
            "status": "error",
            "data": {
                "result": []
            }
        }


# =========================================================
# CPU USAGE
# =========================================================

def get_cpu_usage():

    query = """
    100 * (
      1 - avg(
        rate(node_cpu_seconds_total{mode="idle"}[5m])
      )
    )
    """

    return query_prometheus(query)


# =========================================================
# AVAILABLE RAM
# =========================================================

def get_ram_available():

    query = "node_memory_MemAvailable_bytes"

    return query_prometheus(query)


# =========================================================
# SYSTEM UPTIME
# =========================================================

def get_system_uptime():

    query = "time() - node_boot_time_seconds"

    return query_prometheus(query)


# =========================================================
# DASHBOARD METRICS
# =========================================================

def get_prometheus_metrics():

    metrics = {}

    # CPU
    try:

        cpu_data = get_cpu_usage()

        cpu = float(
            cpu_data["data"]["result"][0]["value"][1]
        )

        metrics["cpu_usage"] = round(cpu, 2)

    except:

        metrics["cpu_usage"] = 0

    # RAM
    try:

        ram_data = get_ram_available()

        ram_bytes = float(
            ram_data["data"]["result"][0]["value"][1]
        )

        ram_gb = ram_bytes / (1024 ** 3)

        metrics["available_ram"] = round(ram_gb, 2)

        metrics["memory_usage"] = round(
            max(0, 100 - ((ram_gb / 8) * 100)),
            2
        )

    except:

        metrics["available_ram"] = 0
        metrics["memory_usage"] = 0

    # Uptime
    try:

        uptime_data = get_system_uptime()

        uptime_seconds = float(
            uptime_data["data"]["result"][0]["value"][1]
        )

        uptime_hours = uptime_seconds / 3600

        metrics["uptime_hours"] = round(
            uptime_hours,
            1
        )

    except:

        metrics["uptime_hours"] = 0

    metrics["network_latency"] = 24

    alerts = get_real_alerts()

    metrics["active_alerts"] = len(alerts)

    return metrics


# =========================================================
# REAL ALERTS
# =========================================================

def get_real_alerts():

    alerts = []

    try:

        cpu_data = get_cpu_usage()

        cpu_value = float(
            cpu_data["data"]["result"][0]["value"][1]
        )

        if cpu_value > 80:

            alerts.append({
                "pod": "node",
                "reason": f"High CPU Usage ({cpu_value:.2f}%)"
            })

    except:
        pass

    try:

        ram_data = get_ram_available()

        ram_bytes = float(
            ram_data["data"]["result"][0]["value"][1]
        )

        ram_gb = ram_bytes / (1024 ** 3)

        if ram_gb < 1:

            alerts.append({
                "pod": "node",
                "reason": f"Low Available RAM ({ram_gb:.2f} GB)"
            })

    except:
        pass

    return alerts


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("\nCPU Usage\n")
    print(get_cpu_usage())

    print("\nRAM Available\n")
    print(get_ram_available())

    print("\nSystem Uptime\n")
    print(get_system_uptime())

    print("\nDashboard Metrics\n")
    print(get_prometheus_metrics())

    print("\nReal Alerts\n")
    print(get_real_alerts())