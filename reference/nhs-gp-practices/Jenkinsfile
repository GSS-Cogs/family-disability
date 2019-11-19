pipeline {
    agent {
        label 'master'
    }
    stages {
        stage('Clean') {
            steps {
                sh 'rm -rf out'
            }
        }
	stage('Fetch') {
	    steps {
		script {
		    def response = httpRequest(contentType: 'APPLICATION_ZIP',
					       httpMode: 'GET',
					       url: 'https://files.digital.nhs.uk/assets/ods/current/epraccur.zip',
					       outputFile: 'epraccur.zip')
		    unzip 'epraccur.zip'
		}
	    }
	}
        stage('Transform') {
            agent {
                docker {
                    image 'gsscogs/csv2rdf'
                    reuseNode true
                    alwaysPull true
                }
            }
            steps {
                script {
                    sh "csv2rdf -m annotated -t epraccur.csv -u reference/nhs-gp-practices/epraccur.csv-metadata.json -o epraccur.ttl"
                }
            }
        }
    }
}
