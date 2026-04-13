pipeline {
    agent any

    stages {

        stage('Fetch Logs from Kubernetes') {
            steps {
                sh '''
                kubectl get pods
                kubectl logs $(kubectl get pods --no-headers | awk '{print $1}' | head -n 1) > logs.txt
                '''
            }
        }

        stage('Run AI Debugging') {
            steps {
                sh 'python3 main.py --file logs.txt'
            }
        }

        stage('Done') {
            steps {
                echo 'Pipeline completed successfully!'
            }
        }
    }
}