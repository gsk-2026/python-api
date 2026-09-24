pipeline {

agent any 

    // Constraint 4: Jenkins handles scheduled execution times for different environments
    triggers {
        cron('''
            0 0 * * 1-5 % ENVIRONMENT=DIT;TEST_SUITE=all
            0 2 * * 6   % ENVIRONMENT=SIT;TEST_SUITE=all
            0 4 1 * *   % ENVIRONMENT=UAT;TEST_SUITE=integration
        ''')
    }

    // Constraint 5b: Allows manual parameter selection in Jenkins interface anytime
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['DIT', 'SIT', 'UAT'], description: 'Target Infrastructure Fleet')
        choice(name: 'TEST_SUITE', choices: ['all', 'integration', 'e2e', 'performance'], description: 'QA Scope Selector')
    }

    environment {
        // Generate a Fine-Grained Personal Access Token (PAT) in GitHub with 'Contents: Write' permissions
        // Add it to Jenkins credentials store under the ID: 'github-api-token'
        GITHUB_TOKEN = credentials('github-api-token')
        REPO_OWNER   = 'gsk-2026'
        REPO_NAME    = 'python-api'
    }

    stages {
        stage('Determine Cron vs Manual Context') {
            steps {
                script {
                    // If triggered by a cron expression, parse out custom environment configuration strings
                    if (currentBuild.getBuildCauses().toString().contains('TimerTrigger')) {
                        echo "Scheduled execution detected. Extracting cron target parameters..."
                        // Note: If using custom cron plugin syntax, parse environmental injections here.
                        // Default fallbacks matched to specific cron timing targets:
                        def hour = new Date().format("H")
                        if (hour == "0") { ENVIRONMENT = "DIT"; TEST_SUITE = "all" }
                        else if (hour == "2") { ENVIRONMENT = "SIT"; TEST_SUITE = "all" }
                        else if (hour == "4") { ENVIRONMENT = "UAT"; TEST_SUITE = "integration" }
                    } else {
                        echo "Manual pipeline execution detected. Processing selector options..."
                        ENVIRONMENT = params.ENVIRONMENT
                        TEST_SUITE  = params.TEST_SUITE
                    }
                    echo "Targeting Environment Suite Context -> [
                        ENVIRONMENT]withScope−>[
                            cap E cap N cap V cap I cap R cap O cap N cap M cap E cap N cap T close bracket w i t h cap S c o p e minus is greater than open bracket 𝐸𝑁𝑉𝐼𝑅𝑂𝑁𝑀𝐸𝑁𝑇
                        ]𝑤𝑖𝑡ℎ𝑆𝑐𝑜𝑝𝑒−>[{TEST_SUITE}
                    ]"
                }
            }
        }

        stage('Dispatch Request to GitHub Action Engine') {
            steps {
                script {
                    def payload = """{
                        "event_type": "jenkins-trigger",
                        "client_payload": {
                            "environment": "\${ENVIRONMENT}",
                            "test_suite": "\${TEST_SUITE}"
                        }
                    }"""

                    // REST Call directly communicating back to the GitHub Dispatch Interface
                    sh """
                        curl -X POST \
                        -H "Accept: application/vnd.github+json" \
                        -H "Authorization: Bearer \${GITHUB_TOKEN}" \
                        -H "X-GitHub-Api-Version: 2022-11-28" \
                        https://api.github.com/repos/\({REPO_OWNER}/\){REPO_NAME}/dispatches \
                        -d '\${payload}'
                    """
                    echo "Payload securely dispatched downstream to GitHub Actions pipeline runner successfully."
                }
            }
        }
    }
}