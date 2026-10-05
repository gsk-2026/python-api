pipeline {
    agent any

    triggers {
        parameterizedCron('''
            # GitHub Actions: Override the default which is in UTC for cron
            TZ=America/Chicago

            # Schedule 1: Full test run for practice_expandtesting_api
            0 22 * * 1-5 %TARGET_TEST_SUITE=practice_expandtesting_api;TARGET_TEST_ENV=DIT;TARGET_TEST_SCOPE=all
            0 22 * * 6   %TARGET_TEST_SUITE=practice_expandtesting_api;TARGET_TEST_ENV=SIT;TARGET_TEST_SCOPE=all
            0 22 * * 7   %TARGET_TEST_SUITE=practice_expandtesting_api;TARGET_TEST_ENV=UAT;TARGET_TEST_SCOPE=integration

            # Schedule 2: Full test run for restful_booker_api
            0 23 * * 1-5 %TARGET_TEST_SUITE=restful_booker_api;TARGET_TEST_ENV=DIT;TARGET_TEST_SCOPE=all
            0 23 * * 6   %TARGET_TEST_SUITE=restful_booker_api;TARGET_TEST_ENV=SIT;TARGET_TEST_SCOPE=all
            0 23 * * 7   %TARGET_TEST_SUITE=restful_booker_api;TARGET_TEST_ENV=UAT;TARGET_TEST_SCOPE=integration
        ''')
    }

    parameters {
        choice(name: 'TARGET_TEST_SUITE', choices: ['practice_expandtesting_api', 'restful_booker_api'], description: 'Target Test Suite')
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
                echo "Targeting Suite -> [${params.TARGET_TEST_SUITE}] | Environment -> [${params.TARGET_TEST_ENV}] | Scope -> [${params.TARGET_TEST_SCOPE}]"
            }
        }

        stage('Dispatch Request to GitHub Action Engine') {
            steps {
                script {
                    def targetTestSuite = params.TARGET_TEST_SUITE
                    def targetTestEnv    = params.TARGET_TEST_ENV
                    def targetTestScope  = params.TARGET_TEST_SCOPE

                    // 1. Single-line minified JSON string to prevent Windows batch multiline line-break errors
                    def payload = "{\"event_type\":\"jenkins-trigger-${targetTestSuite}\",\"client_payload\":{\"jenkins_target_suite\":\"${targetTestSuite}\",\"jenkins_target_env\":\"${targetTestEnv}\",\"jenkins_target_scope\":\"${targetTestScope}\"}}"

                    // 2. Escape double quotes inside Windows bat command and pass GITHUB_TOKEN directly
                    bat """
                        curl --fail-with-body -sS -X POST ^
                        -H "Accept: application/vnd.github+json" ^
                        -H "Authorization: Bearer %GITHUB_TOKEN%" ^
                        -H "X-GitHub-Api-Version: 2022-11-28" ^
                        https://api.github.com/repos/%REPO_OWNER%/%REPO_NAME%/dispatches ^
                        -d "${payload.replace('"', '""')}"
                    """
                    echo "Payload securely dispatched downstream to GitHub Actions runner for suite: ${targetTestSuite}, env: ${targetTestEnv}, scope: ${targetTestScope}."
                }
            }
        }
    }
}