pipeline {
    agent any

    environment {
        DOCKER_USER = "jayantt"
        IMAGE_NAME = "IMT2023523-cicd"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/jayantt23/imt2023523-cicd-lab'
            }
        }

        stage('Build') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_USER/$IMAGE_NAME:latest .'
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                    sh 'docker push $DOCKER_USER/$IMAGE_NAME:latest'
                }
            }
        }
    }
}
