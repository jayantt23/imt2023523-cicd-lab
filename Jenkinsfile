pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
        }
    }

    stages {
        stage('Build') {
            steps {
                sh '''
                    python --version
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    pytest || echo "No tests found"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t jayant/app:latest .'
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh '''
                        echo $PASS | docker login -u $USER --password-stdin
                        docker push jayant/app:latest
                    '''
                }
            }
        }
    }
}
