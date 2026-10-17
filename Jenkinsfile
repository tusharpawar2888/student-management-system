
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                bat 'py -m venv .venv'
                bat '.venv\\Scripts\\python.exe -m pip install --upgrade pip'
                bat '.venv\\Scripts\\python.exe -m pip install -r requirements.txt'
            }
        }

        stage('Automated Testing') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pytest -v'
            }
        }

        stage('Code Quality Check') {
            steps {
                bat '.venv\\Scripts\\python.exe -m flake8 app.py tests/test_app.py'
            }
        }

        stage('Package Application') {
            steps {
                bat '''
                    if exist deploy rmdir /s /q deploy
                    mkdir deploy
                    copy app.py deploy\\app.py
                    copy requirements.txt deploy\\requirements.txt
                    copy Procfile deploy\\Procfile
                    xcopy templates deploy\\templates /E /I /Y
                    xcopy static deploy\\static /E /I /Y
                '''
                archiveArtifacts artifacts: 'deploy/**',
                                 fingerprint: true
            }
        }
    }

    post {
        success {
            echo 'Pipeline successful: tests and quality checks passed; application packaged.'
        }
        failure {
            echo 'Pipeline failed. Check the Console Output for the failing stage.'
        }
    }
}
