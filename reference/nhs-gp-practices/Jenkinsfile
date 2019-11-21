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
                    unzip zipFile: 'epraccur.zip', dir: 'reference/nhs-gp-practices/'
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
                    sh "csv2rdf -m annotated -t reference/nhs-gp-practices/epraccur.csv -u reference/nhs-gp-practices/epraccur.csv-metadata.json -o epraccur.ttl"
                }
            }
        }
	stage('Add concept scheme') {
            steps {
                script {
                    def pmd = pmdConfig('pmd')
                    def draftset = pmd.drafter.listDraftsets().find { it['display-name'] == env.JOB_NAME }
                    if (draftset) {
                        pmd.drafter.deleteDraftset(draftset.id)
                    }
		    String id = pmd.drafter.createDraftset(env.JOB_NAME).id
		    String graph = 'http://gss-data.org.uk/def/concept-scheme/nhs-gp-practices'
		    pmd.drafter.deleteGraph(id, graph)
		    pmd.drafter.addData(id, graph, 'text/ttl', 'UTF-8', 'reference/nhs-gp-practices/epraccur.ttl')
                    pmd.drafter.publishDraftset(id)
                }
            }
        }

    }
}
