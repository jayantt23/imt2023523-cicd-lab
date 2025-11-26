pipeline {
    agent { label 'windows' }
    
    environment {
        DOCKERHUB_USERNAME = 'jayantt'
        IMAGE_NAME = 'IMT2023523-todo-cli'
        IMAGE_TAG = "${BUILD_NUMBER}"

        DOCKERHUB_CREDS = credentials('Docker-Jenkins')
        GITHUB_CREDS    = credentials('github-creds')

        PYTHON = "C:\\Users\\Jayant Sharma\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe"
    }
    
    stages {

        stage('Checkout') {
            steps {
                echo "Pulling code from GitHub..."
                git branch: 'main',
                    url: 'https://github.com/jayantt23/imt2023523-cicd-lab',
                    credentialsId: 'Github-JenkinCreds'
            }
        }

        stage('Build - Install Dependencies') {
            steps {
                echo "Setting up Python virtual environment..."
                bat """
                "%PYTHON%" -m venv venv
                venv\\Scripts\\python.exe -m pip install --upgrade pip
                venv\\Scripts\\python.exe -m pip install -r requirements.txt
                venv\\Scripts\\python.exe -m pip install pytest
                """
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running tests..."
                bat """
                venv\\Scripts\\python.exe -m pytest tests\\test_todo.py -v
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                bat """
                docker build -t %DOCKERHUB_USERNAME%/%IMAGE_NAME%:%IMAGE_TAG% .
                docker build -t %DOCKERHUB_USERNAME%/%IMAGE_NAME%:latest .
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "Authenticating and pushing image to DockerHub..."
                bat """
                docker login -u %DOCKERHUB_CREDS_USR% -p %DOCKERHUB_CREDS_PSW%
                docker push %DOCKERHUB_USERNAME%/%IMAGE_NAME%:%IMAGE_TAG%
                docker push %DOCKERHUB_USERNAME%/%IMAGE_NAME%:latest
                docker logout
                """
            }
        }

        stage('Verify Docker Image') {
            steps {
                echo "Verifying Docker image locally..."
                bat "docker images | findstr %IMAGE_NAME%"
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
        always {
            cleanWs()
        }
    }
}
