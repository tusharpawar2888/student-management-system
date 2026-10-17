pipeline {
    agent any
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Build') { steps { sh 'python --version'; sh 'python -m pip install -r requirements.txt' } }
        stage('Automated Testing') {
            steps { sh 'python -m pytest -v --junitxml=test-results.xml' }
            post { always { junit allowEmptyResults: true, testResults: 'test-results.xml' } }
        }
        stage('Code Quality Check') { steps { sh 'python -m flake8 app.py tests/test_app.py' } }
        stage('Package Application') {
            steps {
                sh 'mkdir -p deploy'
                sh 'cp app.py requirements.txt deploy/'
                sh 'cp -r templates static deploy/'
                archiveArtifacts artifacts: 'deploy/**', fingerprint: true
            }
        }
    }
    post {
        success { echo 'CI passed: tests and code quality checks passed; package archived.' }
        failure { echo 'Pipeline failed. Review Console Output and fix the failing stage.' }
    }
}
