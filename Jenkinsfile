pipeline {
    agent any

    environment {
        containerRegistryName = 'containerregistry1z.azurecr.io'
        dockerImageName = 'stb'
    }

    stages {
        stage('Build and Push Docker Image') {
            steps {
                script {
                    // Get the latest commit hash
                    def hash = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    echo "Commit Hash: ${hash}"
                    
                    // Access the Jenkins build number from the environment variable
                    def buildNumber = env.BUILD_NUMBER
                    echo "Build Number: ${buildNumber}"
                    
                    // Build Docker image with commit hash tag
                    sh "docker build . -t ${dockerImageName}:${hash}"
                    
                    // Tag Docker image with build number
                    sh "docker tag ${dockerImageName}:${hash} ${containerRegistryName}/${dockerImageName}:${buildNumber}"
                    
                    // Docker login and push the image tagged with build number
                    withCredentials([usernamePassword(credentialsId: 'dockerCredentialsId', usernameVariable: 'D_USERNAME', passwordVariable: 'D_PASSWORD')]) {
                        sh "echo ${D_PASSWORD} | docker login ${containerRegistryName} -u ${D_USERNAME} --password-stdin"
                        sh "docker push ${containerRegistryName}/${dockerImageName}:${buildNumber}"
                    }
                }
            }
        }
        
        stage('Pull and Run Docker Image') {
            steps {
                script {
                    // Pull the Docker image using the build number
                    sh "docker pull ${containerRegistryName}/${dockerImageName}:${env.BUILD_NUMBER}"
                    
                    // Run the Docker container with the pulled image
                    sh "docker run --name stb -d -p 8501:8501 ${containerRegistryName}/${dockerImageName}:${env.BUILD_NUMBER}"
                }
            }
        }
    }
}
