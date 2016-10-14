def token = 'fIFVFOGfj5a9g2LLKaeuXZ_LWWGe7yAICoj6GCWehaU'
node {
	stage('Checkout') {
		checkout scm
		sh 'ls -la'
	}
	
	def app = null
	docker.withServer('tcp://192.168.100.160:2375') {
		
		stage('Build Docker') {
			app = docker.build "192.168.100.160:5000/trex-demo-stage/service-a:latest"
		}
		stage('Unit Test') {
			def testResult = app.withRun('-v "`pwd`":/code/results','./test.sh') { c ->
				sh 'whoami'
			}
			echo testResult
			//junit 'nose2-junit.xml'
		}

		stage('Staging Environment') {
			app.push()
			sshagent('ssh-creds') {
				sh 'ssh -o StrictHostKeyChecking=no -l cloudbees 192.168.10.80 uname -a'
			}
		}


	}
}
	
