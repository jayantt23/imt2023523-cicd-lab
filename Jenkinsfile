pipeline {
    agent any

    environment {
        DOCKER_USER = "jayantt"
        IMAGE_NAME = "imt2023523-cicd"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/jayantt23/imt2023523-cicd-lab'
            }
        }

        stage('Build') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                bat 'pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %DOCKER_USER%/%IMAGE_NAME%:latest .'
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                 usernameVariable: 'USER',
                                                 passwordVariable: 'PASS')]) {
                    bat 'echo %PASS% | docker login -u %USER% --password-stdin'
                    bat 'docker push %DOCKER_USER%/%IMAGE_NAME%:latest'
                }
            }
        }
    }
}
