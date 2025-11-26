pipeline {
    agent any
    
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

        stage('Install Dependencies') {
            steps {
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
                bat """
                venv\\Scripts\\python.exe -m pytest tests\\test_todo.py -v
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                bat """
                docker build -t %DOCKERHUB_USERNAME%/%IMAGE_NAME%:%IMAGE_TAG% .
                docker build -t %DOCKERHUB_USERNAME%/%IMAGE_NAME%:latest .
                """
            }
        }

        stage('Push to DockerHub') {
            steps {
                bat """
                docker login -u %DOCKERHUB_CREDS_USR% -p %DOCKERHUB_CREDS_PSW%
                docker push %DOCKERHUB_USERNAME%/%IMAGE_NAME%:%IMAGE_TAG%
                docker push %DOCKERHUB_USERNAME%/%IMAGE_NAME%:latest
                docker logout
                """
            }
        }
    }

    post {
        always {
            echo "Cleaning workspace..."
            deleteDir()
        }
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
