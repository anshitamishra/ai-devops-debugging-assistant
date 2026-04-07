pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/anshitamishra/ai-devops-debugging-assistant.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing dependencies..."
            }
        }

        stage('Run Application') {
            steps {
                echo "Running DevOps Assistant..."
                sh 'python main.py --log "CrashLoopBackOff error"'
            }
        }

        stage('Kubernetes Check') {
            steps {
                echo "Checking Kubernetes pods..."
                sh 'kubectl get pods'
            }
        }
    }
}