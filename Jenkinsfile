pipeline {
    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    parameters {
        choice(
            name: 'TARGET_ENV',
            choices: ['sit', 'uat', 'prod'],
            description: 'Environment to run tests against'
        )
        string(
            name: 'PYTEST_MARKER',
            defaultValue: '',
            description: 'Optional pytest marker, for example: e2e or api_validation'
        )
    }

    environment {
        VENV_DIR = '.venv'
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Virtualenv') {
            steps {
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run API Tests') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    if [ -n "${PYTEST_MARKER}" ]; then
                        python -m pytest --env="${TARGET_ENV}" -m "${PYTEST_MARKER}"
                    else
                        python -m pytest --env="${TARGET_ENV}"
                    fi
                '''
            }
        }
    }
}
