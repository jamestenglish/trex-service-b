node {
	stage 'Checkout'
	checkout scm

	
	docker.withServer('tcp://192.168.100.160:2375') {
		stage 'Build Docker'
		def app = docker.build "172.30.122.20:5000/trex-demo-stage/service-a:latest"

		stage 'Unit Test'
		def testResult = app.withRun('','py.test --junitxml result.xml tests.py && cat results.xml') { c ->
			sh 'whoami'
		}
		sh "echo ${testResult} > results.xml"
		junit '*.xml'

		stage 'Staging Environment'
		app.push()


	}
}
	
