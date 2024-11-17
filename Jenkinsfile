pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/Doron126/Jenkins-Docker-Flask-app.git'
            }
        }
        stage('Setup Environment') {
            steps {
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }
        stage('Run Flask App') {
            steps {
                sh '''
                source venv/bin/activate
                python app.py &
                APP_PID=$!
                sleep 5
                curl -I http://127.0.0.1:5000 || (echo "Flask app test failed" && exit 1)
                kill $APP_PID
                '''
            }
        }
    }
}
