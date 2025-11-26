pipeline {
    agent any

    environment {
        IMAGE = "jayantt23/IMT2023523-todo-cli:latest"
        VENV = ".venv"
        PYTHON = "python3"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh """
                    $PYTHON --version
                    $PYTHON -m venv $VENV
                    . $VENV/bin/activate
                    pip install --upgrade pip
                """
            }
        }

        stage('Lint') {
            steps {
                sh """
                    . $VENV/bin/activate
                    pip install flake8
                    flake8 todo.py tests/test_todo.py --count --select=E9,F63,F7,F82 --show-source --statistics
                """
            }
        }

        stage('Test') {
            steps {
                sh """
                    . $VENV/bin/activate
                    pip install pytest pytest-cov
                    python3 -m pytest tests/test_todo.py -v --junitxml=test-results.xml --cov=todo --cov-report=xml:coverage.xml
                """
            }
            post {
                always {
                    junit 'test-results.xml'
                    archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t $IMAGE ."
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'jayantt23', 
                                                  usernameVariable: 'DOCKER_USER', 
                                                  passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $IMAGE
                        docker logout
                    """
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}
