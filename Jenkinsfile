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

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t employee-management-app .'
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                    docker rm -f employee-test || true

                    docker run -d \
                        --name employee-test \
                        --restart unless-stopped \
                        -p 5000:5000 \
                        -e DATABASE_PATH=/data/employees.db \
                        -v employee-data:/data \
                        employee-management-app:latest
                '''
            }
        }
    }
}
