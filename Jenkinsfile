pipeline {
    agent any

    stages {

        stage('Clone Repo') {
            steps {
                echo 'Cloning repository...'
            }
        }

        stage('Run AI Debugging') {
            steps {
                bat 'python main.py --log "CrashLoopBackOff error"'
            }
        }

        stage('Done') {
            steps {
                echo 'Pipeline completed successfully!'
            }
        }
    }
}