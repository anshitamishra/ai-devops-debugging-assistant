pipeline {
    agent any

    stages {

        stage('Fetch Logs from Kubernetes') {
            steps {
                sh '''
                echo "Fetching Kubernetes Pods..."
                kubectl get pods

                echo "Selecting failing pod..."

                POD_INFO=$(kubectl get pods --no-headers | grep -E "CrashLoopBackOff|ImagePullBackOff|OOMKilled" | head -n 1)

                if [ -z "$POD_INFO" ]; then
                    echo "No failing pod found, selecting first pod..."
                    POD=$(kubectl get pods --no-headers | awk '{print $1}' | head -n 1)
                    kubectl logs $POD > logs.txt || true
                else
                    POD=$(echo $POD_INFO | awk '{print $1}')
                    STATUS=$(echo $POD_INFO | awk '{print $3}')

                    echo "Selected Pod: $POD"
                    echo "Status: $STATUS"

                    if [[ "$STATUS" == "ImagePullBackOff" ]]; then
                        echo "Using describe for ImagePullBackOff..."
                        kubectl describe pod $POD > logs.txt
                    else
                        echo "Using logs for running/crashing pod..."
                        kubectl logs $POD > logs.txt || true
                    fi
                fi
                '''
            }
        }

        stage('Run AI Debugging') {
            steps {
                sh '''
                echo "Running AI Debugging Assistant..."
                python3 main.py --file logs.txt
                '''
            }
        }

        stage('Done') {
            steps {
                echo 'Pipeline completed successfully!'
            }
        }
    }
}