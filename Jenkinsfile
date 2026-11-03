pipeline {
  agent any
  triggers { pollSCM('H/5 * * * *') }
  options { timestamps(); timeout(time: 10, unit: 'MINUTES'); buildDiscarder(logRotator(numToKeepStr: '10')) }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Test') { steps { sh 'mvn -B -ntp clean test' } }
    stage('Package') { steps { sh 'mvn -B -ntp -DskipTests package' } }
  }
  post {
    always { junit testResults: 'target/surefire-reports/*.xml', allowEmptyResults: false }
    success { archiveArtifacts artifacts: 'target/mini-inventory.jar', fingerprint: true }
  }
}
