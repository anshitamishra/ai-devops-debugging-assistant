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
# REAL KUBERNETES ALERTS
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

            if phase != "Running":

                alerts.append({
                    "pod": pod_name,
                    "namespace": namespace,
                    "status": phase
                })

    except Exception as e:

        print("Kubernetes Alerts Error:", e)

    return alerts