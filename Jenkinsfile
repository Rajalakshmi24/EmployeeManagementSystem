pipeline {
    agent any

    stages {
        
        stage('Python Version') {
            steps {
                sh 'python3 --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv .venv'
                sh '.venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Validate Application') {
            steps {
                sh '.venv/bin/python -m compileall -q app.py'
                echo 'Python syntax validation successful!'
            }
        }
    }
}