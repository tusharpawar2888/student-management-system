
pipeline {
    agent any

    environment {
        PYTHON = 'C:/Users/HP/AppData/Local/Python/bin/python.exe'
    }

    stages {
        stage('Build') {
            steps {
                bat '"%PYTHON%" --version'
                bat '"%PYTHON%" -m pip install -r requirements.txt'
            }
        }

        stage('Automated Testing') {
            steps {
                bat '"%PYTHON%" -m pytest -v --junitxml=test-results.xml'
            }
            post {
                always {
                    junit allowEmptyResults: true,
                          testResults: 'test-results.xml'
                }
            }
        }

        stage('Code Quality Check') {
            steps {
                bat '"%PYTHON%" -m flake8 app.py tests/test_app.py'
            }
        }

        stage('Deployment') {
            steps {
                bat 'if not exist deploy mkdir deploy'
                bat 'copy /Y app.py deploy\\app.py'
                bat 'copy /Y requirements.txt deploy\\requirements.txt'
                archiveArtifacts artifacts: 'deploy/*',
                                 fingerprint: true
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}
