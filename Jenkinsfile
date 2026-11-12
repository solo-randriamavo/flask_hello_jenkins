pipeline {
    agent {
        kubernetes {
            label 'jenkins-agent-my-app'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    component: ci
spec:
  containers:
    - name: python
      image: python:3.12-slim
      command:
        - cat
      tty: true
"""
        }
    }

    stages {
        stage('Test Python') {
            steps {
                container('python') {
                    sh 'python --version'
                    sh 'pip install --no-cache-dir -r requirements.txt'
                    sh 'python test.py --verbose'
                }
            }
        }
    }
}
