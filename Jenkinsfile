pipeline {
    agent any

    environment {
        KUBECONFIG = '/var/jenkins_home/.kube/config'
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/anshitamishra/ai-devops-debugging-assistant.git'
            }
        }

        stage('Verify Files') {
            steps {
                echo "Checking project files..."
                sh 'ls'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying application to Kubernetes..."
                sh '''
                kubectl apply -f deployment.yaml --validate=false
                kubectl apply -f service.yaml --validate=false
                '''
            }
        }

        stage('Check Kubernetes Pods') {
            steps {
                echo "Fetching pod status..."
                sh 'kubectl get pods'
            }
        }

        stage('Run AI Debugging Assistant') {
            steps {
                echo "Running AI DevOps Debugging Assistant..."
                sh '''
                python3 main.py --pod plane-worker-wl-6cf9fb4f8b-dm4dj
                '''
            }
        }
    }
}
