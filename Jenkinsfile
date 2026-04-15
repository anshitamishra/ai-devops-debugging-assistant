pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                echo "Cloning repository..."
            }
        }

        stage('Build') {
            steps {
                echo "Building application..."
            }
        }

        stage('Validate') {
            steps {
                echo "Validating configuration..."
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                kubectl apply -f deployment.yaml
                '''
            }
        }

        stage('Fetch Logs from Kubernetes') {
            steps {
                sh '''
                echo Fetching Kubernetes Pods...
                kubectl get pods

                POD_INFO=$(kubectl get pods --no-headers | grep -E "CrashLoopBackOff|ImagePullBackOff|OOMKilled" | head -n 1)

                if [ -z "$POD_INFO" ]; then
                    echo "No failing pod found. Taking first pod."
                    POD=$(kubectl get pods --no-headers | awk '{print $1}' | head -n 1)
                    STATUS="Running"
                else
                    POD=$(echo $POD_INFO | awk '{print $1}')
                    STATUS=$(echo $POD_INFO | awk '{print $3}')
                fi

                echo "Selected Pod: $POD"
                echo "Status: $STATUS"

                if [ "$STATUS" = "ImagePullBackOff" ]; then
                    kubectl describe pod $POD > logs.txt || true
                else
                    kubectl logs $POD > logs.txt || true
                fi
                '''
            }
        }

        stage('Run AI Debugging') {
            steps {
                sh '''
                echo Running AI Debugging Assistant...
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
pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                echo "Cloning repository..."
            }
        }

        stage('Build') {
            steps {
                echo "Building application..."
            }
        }

        stage('Validate') {
            steps {
                echo "Validating configuration..."
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                kubectl apply -f deployment.yaml
                '''
            }
        }

        stage('Fetch Logs from Kubernetes') {
            steps {
                sh '''
                echo Fetching Kubernetes Pods...
                kubectl get pods

                POD_INFO=$(kubectl get pods --no-headers | grep -E "CrashLoopBackOff|ImagePullBackOff|OOMKilled" | head -n 1)

                if [ -z "$POD_INFO" ]; then
                    echo "No failing pod found. Taking first pod."
                    POD=$(kubectl get pods --no-headers | awk '{print $1}' | head -n 1)
                    STATUS="Running"
                else
                    POD=$(echo $POD_INFO | awk '{print $1}')
                    STATUS=$(echo $POD_INFO | awk '{print $3}')
                fi

                echo "Selected Pod: $POD"
                echo "Status: $STATUS"

                if [ "$STATUS" = "ImagePullBackOff" ]; then
                    kubectl describe pod $POD > logs.txt || true
                else
                    kubectl logs $POD > logs.txt || true
                fi
                '''
            }
        }

        stage('Run AI Debugging') {
            steps {
                sh '''
                echo Running AI Debugging Assistant...
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