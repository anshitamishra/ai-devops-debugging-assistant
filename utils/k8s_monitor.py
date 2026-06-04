from kubernetes import client, config

# =========================================================
# CLUSTER HEALTH
# =========================================================

def get_cluster_health():

    try:

        config.load_kube_config()

        v1 = client.CoreV1Api()

        nodes = v1.list_node().items
        pods = v1.list_pod_for_all_namespaces().items

        healthy_nodes = len(nodes)

        running_pods = 0

        for pod in pods:

            if pod.status.phase == "Running":
                running_pods += 1

        return {
            "nodes": healthy_nodes,
            "pods": running_pods,
            "status": "Healthy"
        }

    except Exception as e:

        print("Kubernetes Connection Error:", e)

        return {
            "nodes": 1,
            "pods": 34,
            "status": "Demo Mode"
        }


# =========================================================
# KUBERNETES ALERTS
# =========================================================

def get_kubernetes_alerts():

    alerts = []

    try:

        config.load_kube_config()

        v1 = client.CoreV1Api()

        pods = v1.list_pod_for_all_namespaces().items

        for pod in pods:

            pod_name = pod.metadata.name
            namespace = pod.metadata.namespace

            phase = pod.status.phase

            # Detect container-level failures
            container_statuses = pod.status.container_statuses

            if container_statuses:

                for container in container_statuses:

                    if container.state.waiting:

                        reason = container.state.waiting.reason

                        if reason in [
                            "CrashLoopBackOff",
                            "ImagePullBackOff",
                            "ErrImagePull",
                            "CreateContainerConfigError"
                        ]:

                            alerts.append({
                                "pod": pod_name,
                                "namespace": namespace,
                                "status": reason
                            })

            # Detect pod-level issues
            if phase in [
                      "Pending",
                      "Failed",
                      "Unknown"
                    ]: 

                alerts.append({
                    "pod": pod_name,
                    "namespace": namespace,
                    "status": phase
                })

    except Exception as e:

        print("Kubernetes Alerts Error:", e)

    return alerts


# =========================================================
# FETCH LIVE POD LOGS
# =========================================================

def get_pod_logs(namespace, pod_name, tail_lines=100):

    try:

        config.load_kube_config()

        v1 = client.CoreV1Api()

        logs = v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            tail_lines=tail_lines
        )

        return logs

    except Exception:

        return f"""
Kubernetes Incident Detected

Namespace: {namespace}
Pod: {pod_name}

Container logs unavailable.

Likely causes:
- ImagePullBackOff
- ErrImagePull
- CrashLoopBackOff
- Pending Container
- Startup Failure
"""
    
# =========================================================
# AUTO INCIDENT COLLECTION
# =========================================================

def get_live_incidents():

    incidents = []

    alerts = get_kubernetes_alerts()

    for alert in alerts:

        logs = get_pod_logs(
            alert["namespace"],
            alert["pod"]
        )

        incidents.append({
            "pod": alert["pod"],
            "namespace": alert["namespace"],
            "status": alert["status"],
            "logs": logs
        })

    return incidents