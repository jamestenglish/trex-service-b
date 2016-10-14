def token = 'fIFVFOGfj5a9g2LLKaeuXZ_LWWGe7yAICoj6GCWehaU'
node {
	stage('Checkout') {
		checkout scm
		sh 'ls -la'
	}
	
	
	docker.withServer('tcp://192.168.100.160:2375') {
		stage('Build Docker') {
			def app = docker.build "172.30.122.20:5000/trex-demo-stage/service-a:latest"
		}
		stage('Unit Test') {
			def testResult = app.withRun('-v "`pwd`":/code/results','./test.sh') { c ->
				sh 'whoami'
			}
			sh 'touch *.xml'
			junit '*.xml'
		}

		stage('Staging Environment') {
			sh "docker login -u test -e test@test.com -p ${token} 172.30.122.20:5000"
			app.push()
		}


	}
}
	
