pipeline {
    agent any

    stages {

        stage('Run AI Debugging') {
            steps {
                sh 'python3 main.py --log "CrashLoopBackOff error"'
            }
        }

        stage('Done') {
            steps {
                echo 'Pipeline completed successfully!'
            }
        }
    }
}