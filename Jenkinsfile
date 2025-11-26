pipeline {
    agent any
    
    environment {
        DOCKERHUB_USERNAME = 'jayantt'
        IMAGE_NAME = 'IMT2023523-todo-cli'
        IMAGE_TAG = "${BUILD_NUMBER}"

        DOCKERHUB_CREDS = credentials('Docker-Jenkins')
        GITHUB_CREDS    = credentials('github-creds')
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/jayantt23/imt2023523-cicd-lab',
                    credentialsId: 'github-creds'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest tests/test_todo.py -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $DOCKERHUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG .
                docker build -t $DOCKERHUB_USERNAME/$IMAGE_NAME:latest .
                '''
            }
        }

        stage('Push to DockerHub') {
            steps {
                sh '''
                echo "$DOCKERHUB_CREDS_PSW" | docker login -u "$DOCKERHUB_CREDS_USR" --password-stdin
                docker push $DOCKERHUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG
                docker push $DOCKERHUB_USERNAME/$IMAGE_NAME:latest
                docker logout
                '''
            }
        }

        stage('Verify Docker Image') {
            steps {
                sh "docker images | grep $IMAGE_NAME"
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
