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
    - name: docker
      image: docker:cli
      command:
        - cat
      tty: true
      volumeMounts:
        - mountPath: /var/run/docker.sock
          name: docker-sock
  volumes:
    - name: docker-sock
      hostPath:
        path: /var/run/docker.sock
"""
        }
    }

    triggers {
        pollSCM('* * * * *')
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

        stage('Build image') {
            steps {
                container('docker') {
                    sh 'docker version'
                    sh 'docker build -t localhost:4000/pythontest:latest .'
                    sh 'docker push localhost:4000/pythontest:latest'
                }
            }
        }
    }
}