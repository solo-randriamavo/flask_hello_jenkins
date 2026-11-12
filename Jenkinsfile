pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
metadata:
  namespace: jenkins
  labels:
    component: ci
spec:
  serviceAccountName: jenkins-deployer
  containers:
    - name: python
      image: python:3.12-slim
      command:
        - cat
      tty: true
    - name: docker-daemon
      image: docker:dind
      args:
        - --insecure-registry=host.minikube.internal:4000
      env:
        - name: DOCKER_TLS_CERTDIR
          value: ""
      securityContext:
        privileged: true
      volumeMounts:
        - name: docker-storage
          mountPath: /var/lib/docker
    - name: docker
      image: docker:cli
      command:
        - cat
      tty: true
      env:
        - name: DOCKER_HOST
          value: tcp://localhost:2375
    - name: kubectl
      image: alpine:3.22
      command:
        - cat
      tty: true
  volumes:
    - name: docker-storage
      emptyDir: {}
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
                    sh '''
                        for attempt in $(seq 1 30); do
                            if docker info >/dev/null 2>&1; then
                                docker version
                                exit 0
                            fi
                            sleep 2
                        done
                        echo "Docker daemon did not become ready"
                        exit 1
                    '''
                    sh 'docker build -t host.minikube.internal:4000/pythontest:latest .'
                    sh 'docker push host.minikube.internal:4000/pythontest:latest'
                }
            }
        }

        stage('Deploy') {
            steps {
                container('kubectl') {
                    sh '''
                        set +x
                        wget -q -O /tmp/kubectl https://dl.k8s.io/release/v1.37.0/bin/linux/amd64/kubectl
                        chmod +x /tmp/kubectl
                        TOKEN="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"
                        CA="/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
                        SERVER="https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT}"

                        /tmp/kubectl \
                          --server="$SERVER" \
                          --certificate-authority="$CA" \
                          --token="$TOKEN" \
                          apply -f kubernetes/deployment.yaml

                        /tmp/kubectl \
                          --server="$SERVER" \
                          --certificate-authority="$CA" \
                          --token="$TOKEN" \
                          apply -f kubernetes/service.yaml
                    '''
                }
            }
        }
    }
}
