pipeline {
    agent any

    stages {

        stage('Fetch Logs from Kubernetes') {
            steps {
                sh '''
                echo "Fetching Kubernetes Pods..."
                kubectl get pods

                echo "Selecting failing pod..."

                POD=$(kubectl get pods --no-headers | grep -E "CrashLoopBackOff|ImagePullBackOff" | awk '{print $1}' | head -n 1)

                if [ -z "$POD" ]; then
                    echo "No failing pod found, selecting first pod..."
                    POD=$(kubectl get pods --no-headers | awk '{print $1}' | head -n 1)
                fi

                echo "Selected Pod: $POD"

                kubectl logs $POD > logs.txt
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