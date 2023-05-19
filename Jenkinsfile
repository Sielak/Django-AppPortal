def getEnvFromBranch(branch) {
  if (branch == 'master') {
    return 'BMA-APP-101'
  } else if (branch == 'test') {
    return 'BMA-APP-701'
  } else {
    return 'BMA-DEV-704'
 }
}

def choosed_agent = getEnvFromBranch(env.BRANCH_NAME)

pipeline {
    agent {
        label "${choosed_agent}"
    }
    options {
        gitLabConnection('gitlab')
        gitlabBuilds(builds: ['Build', 'Test', 'Deploy'])
    }
    stages {
		stage('Build') {
			steps {
                updateGitlabCommitStatus name: 'Build', state: 'pending'
                sh '''
                    . /home/ubuntu/virtual_environments/venv_AppPortal/bin/activate
                    pip install -r requirements.txt
                '''
                updateGitlabCommitStatus name: 'Build', state: 'success'
			}
		}
        stage('Test') {
			steps {
                updateGitlabCommitStatus name: 'Test', state: 'pending'
                sh '''
                    . /home/ubuntu/virtual_environments/venv_AppPortal/bin/activate
                    coverage run --source=. -m pytest
                '''
                updateGitlabCommitStatus name: 'Test', state: 'success'
			}
		}
        stage('Backup_db') {
			steps {
                sh 'cp /opt/AppPortal/db.sqlite3 /home/ubuntu/backup/AppPortal/db.sqlite3'
			}
		}
        stage('Deploy') {
            when { 
                anyOf { 
                    branch 'master'; 
                    branch 'test' 
                } 
            }
			steps {
                updateGitlabCommitStatus name: 'Deploy', state: 'pending'
                sh 'sudo rm -rf /opt/AppPortal/'
                sh 'sudo mkdir /opt/AppPortal'
                sh 'sudo mv * /opt/AppPortal'
                // move db back to project
                sh 'sudo mv /home/ubuntu/backup/AppPortal/db.sqlite3 /opt/AppPortal/db.sqlite3'
                sh 'sudo chown ubuntu:ubuntu /opt/AppPortal/'
                //apply migrations on db
                sh '''
                    . /home/ubuntu/virtual_environments/venv_AppPortal/bin/activate
                    cd /opt/AppPortal && python manage.py collectstatic --noinput
                    cd /opt/AppPortal && python manage.py makemigrations
                    cd /opt/AppPortal && python manage.py migrate
                '''
                sh 'ln -s /media/CrossDocking /opt/AppPortal/static/CrossDocking'
                sh 'ln -s /media/InvestmentRequest /opt/AppPortal/static/InvestmentRequest'
                sh 'sudo service apache2 restart'
                echo 'New version installed'
                updateGitlabCommitStatus name: 'Deploy', state: 'success'
			}
		}
        stage('Deploy - dev') {
            when { 
                not { 
                    anyOf { 
                        branch 'master'; 
                        branch 'test' 
                    } 
                } 
            }
            steps {
                updateGitlabCommitStatus name: 'Deploy', state: 'pending'
                echo 'Inform GitLab pipeline about status of dev build'
                updateGitlabCommitStatus name: 'Deploy', state: 'success'
            }
        }
    }
    post {
        always {
            cleanWs deleteDirs: true, notFailBuild: true
        }
		failure{			
			emailext body: "Job Failed<br>URL: ${env.BUILD_URL}", 
                    recipientProviders: [[$class: 'DevelopersRecipientProvider']],
					subject: "Job: ${env.JOB_NAME}, Build: #${env.BUILD_NUMBER} - Failure !",
					attachLog: true
        }
        success{			
			emailext body: "Job builded<br>URL: ${env.BUILD_URL}", 
                    recipientProviders: [[$class: 'DevelopersRecipientProvider']],
					subject: "Job: ${env.JOB_NAME}, Build: #${env.BUILD_NUMBER} - Success !",
					attachLog: true
        }
    }
}
