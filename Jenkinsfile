def registryTag = 'trex-demo-stage/service-b:latest'
def prodRegistryTag = 'trex-demo-prod/service-b:latest'
def dockerServer = 'tcp://192.168.100.160:2375'
node {
	stage('Checkout') {
		checkout scm
		sh 'ls -la'
		sh "echo \"VERSION = ${env.BUILD_NUMBER}\" > version.py"
	}
	
	def app = null
	docker.withServer(dockerServer) {
		
		stage('Build Docker') {
			app = docker.build "192.168.100.160:5000/${registryTag}"
		}
		stage('Unit Test') {
			
			sshagent(['ssh-cred-1']) {
				sh "ssh -o StrictHostKeyChecking=no -l englishja 192.168.100.160 mkdir test-b"
				sh "ssh -o StrictHostKeyChecking=no -l englishja 192.168.100.160 docker run -v /home/englishja/test-b:/code/results 192.168.100.160:5000/${registryTag} /bin/bash ./test.sh"
				def testResult = sh(script: "ssh -o StrictHostKeyChecking=no -l englishja 192.168.100.160 cat test-b/nose2-junit.xml", returnStdout: true).trim()
				echo testResult
				sh "ssh -o StrictHostKeyChecking=no -l englishja 192.168.100.160 rm  test-b/nose2-junit.xml"
				writeFile(file: "nose2-junit.xml", text: testResult)
			}
			junit 'nose2-junit.xml'
		}

		stage('Staging Environment') {
			app.push()
			sshagent(['ssh-creds']) {
				sh "ssh -o StrictHostKeyChecking=no -l saicadm 192.168.100.80 sudo docker pull 192.168.100.160:5000/${registryTag}"
				sh "ssh -o StrictHostKeyChecking=no -l saicadm 192.168.100.80 sudo docker tag -f 192.168.100.160:5000/${registryTag} 172.30.122.20:5000/${registryTag}"
				def token = sh(script: 'ssh -o StrictHostKeyChecking=no -l saicadm 192.168.100.80 oc whoami -t', returnStdout: true).trim()
				echo token
				sh "ssh -o StrictHostKeyChecking=no -l saicadm 192.168.100.80 \"sudo docker login -u test -e test@test.com -p ${token} 172.30.122.20:5000 && sudo docker push 172.30.122.20:5000/${registryTag}\""
			}
		}
		
		stage('Integration Test') {
			def maxCount = 0
			while(maxCount <= 60) {
				def result = sh(script: "curl http://service-b-trex-demo-stage.router.default.svc.cluster.local/v", returnStdout: true).trim() 
				if(result == "${env.BUILD_NUMBER}") {
					break
				}
				sleep(1)
			}
			if(maxCount >= 60) {
				sh 'false'
			}
		}
		
		stage('Prod Environment') {
			sshagent(['ssh-creds']) {
				sh "ssh -o StrictHostKeyChecking=no -l saicadm 192.168.100.80 sudo docker tag -f 192.168.100.160:5000/${registryTag} 172.30.122.20:5000/${prodRegistryTag}"
				def token = sh(script: 'ssh -o StrictHostKeyChecking=no -l saicadm 192.168.100.80 oc whoami -t', returnStdout: true).trim()
				echo token
				sh "ssh -o StrictHostKeyChecking=no -l saicadm 192.168.100.80 \"sudo docker login -u test -e test@test.com -p ${token} 172.30.122.20:5000 && sudo docker push 172.30.122.20:5000/${prodRegistryTag}\""
			}
		}

	}
}
	
