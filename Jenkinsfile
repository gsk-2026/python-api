pipeline {
    agent any 

    // Jenkins scheduled execution times for different environments
    triggers {
        parameterizedCron('''
            # Schedule 1: Full test run for practice_expandtesting_api
            0 0 * * 1-5 % TARGET_TEST_MODULE=practice_expandtesting_api; TARGET_TEST_ENV=DIT; TARGET_TEST_SCOPE=all
            0 1 * * 6   % TARGET_TEST_MODULE=practice_expandtesting_api; TARGET_TEST_ENV=SIT; TARGET_TEST_SCOPE=all
            0 2 1 * *   % TARGET_TEST_MODULE=practice_expandtesting_api; TARGET_TEST_ENV=UAT; TARGET_TEST_SCOPE=integration

            # Schedule 2: Full test run for new_a_api
            30 0 * * 1-5 % TARGET_TEST_MODULE=new_a_api; TARGET_TEST_ENV=DIT; TARGET_TEST_SCOPE=all
            30 1 * * 6   % TARGET_TEST_MODULE=new_a_api; TARGET_TEST_ENV=SIT; TARGET_TEST_SCOPE=all
            30 2 1 * *   % TARGET_TEST_MODULE=new_a_api; TARGET_TEST_ENV=UAT; TARGET_TEST_SCOPE=integration
        ''')
    }

    // User Manual execution from Jenkins anytime
    parameters {
        choice(name: 'TARGET_TEST_MODULE', choices: ['practice_expandtesting_api', 'new_a_api', 'new_b_api'], description: 'Target Test Module')
        choice(name: 'TARGET_TEST_ENV', choices: ['DIT', 'SIT', 'UAT'], description: 'Target Test Environment')
        choice(name: 'TARGET_TEST_SCOPE', choices: ['all', 'integration', 'e2e', 'performance'], description: 'Target Test Scope')
    }

    environment {
        GITHUB_TOKEN = credentials('github-python-api-token')
        REPO_OWNER   = 'gsk-2026'
        REPO_NAME    = 'python-api'
    }

    stages {
        stage('Log Run Context') {
            steps {
                echo "Targeting Module -> [${params.TARGET_TEST_MODULE}] | Environment -> [${params.TARGET_TEST_ENV}] | Scope -> [${params.TARGET_TEST_SCOPE}]"
            }
        }

        stage('Dispatch Request to GitHub Action Engine') {
            steps {
                script {
                    // Extract parameters directly (parameterizedCron sets params automatically)
                    def targetTestModule = params.TARGET_TEST_MODULE
                    def targetTestEnv    = params.TARGET_TEST_ENV
                    def targetTestScope  = params.TARGET_TEST_SCOPE

                    def payload = """{
                        "event_type": "jenkins-trigger",
                        "client_payload": {
                            "target_module": "${targetTestModule}",
                            "target_env": "${targetTestEnv}",
                            "target_scope": "${targetTestScope}"
                        }
                    }"""

                    // REST Call directly communicating back to the GitHub Repository Dispatch API
                    sh """
                        curl -X POST \
                        -H "Accept: application/vnd.github+json" \
                        -H "Authorization: Bearer \$GITHUB_TOKEN" \
                        -H "X-GitHub-Api-Version: 2022-11-28" \
                        https://api.github.com/repos/\$REPO_OWNER/\$REPO_NAME/dispatches \
                        -d '${payload}'
                    """
                    echo "Payload securely dispatched downstream to GitHub Actions runner for module: ${targetTestModule}."
                }
            }
        }
    }
}