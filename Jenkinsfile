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

        stage('Clone Plane Repo') {
            steps {
                sh '''
                echo "Cloning Plane Repository..."

                if [ ! -d "plane-devops-project" ]; then
                    git clone https://github.com/anshitamishra/plane-devops-project.git
                else
                    echo "Repo already exists, pulling latest changes..."
                    cd plane-devops-project
                    git pull
                fi
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                echo "Deploying Plane app to Kubernetes..."
                cd plane-devops-project

                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml
                '''
            }
        }

        stage('Fetch Logs from Kubernetes') {
            steps {
                sh '''
                echo "Fetching Kubernetes Pods..."
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
                    echo "Using describe for ImagePullBackOff..."
                    kubectl describe pod $POD > logs.txt || true
                else
                    echo "Using logs for pod..."
                    kubectl logs $POD > logs.txt || true
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