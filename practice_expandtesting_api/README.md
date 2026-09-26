# Practice ExpandTesting API Automation Module

This is an independent, self-contained API testing microservice framework built to validate the endpoints provided by the ExpandTesting practice platform. It operates autonomously within the parent repository, maintaining its own isolated configuration, dependency manifests, and runtime logging layers.

##  Background & Purpose

The purpose of this testing module is to ensure the functional health, schema reliability, and security contracts of the production REST APIs hosted on the **[ExpandTesting Practice Portal](https://expandtesting.com)**, **[Notes API Documentation](https://practice.expandtesting.com/notes/api/api-docs/#/)**.

As a dedicated QA exercise application, the application simulates realistic, multi-tiered technical environments. This test automation suite targets critical microservice subsets across integration, end-to-end, and performance layers:
* **User Authentication & Session Tokens:** Verifying user registration, login, logout, profile updates, password modification, and account deletion workflows.
* **Core Business Logic (Notes Application):** Programmatically asserting database persistence contracts—specifically verifying CRUD operations (POST, GET, PUT, PATCH, DELETE) for the notes service.
* **System Stability & Authorization:** Validating token verification filters and component-level baseline health checks (`/health-check`).

By treating this module as an isolated test-bed framework, we simulate microservice-specific behavioral checks without polluting code boundaries or mixing unrelated package dependencies.

---

##  Getting Started & Source Code Download

Follow these sequential steps to clone the codebase from GitHub, set up your development environment, and prepare the project workspaces.

### 1. Clone the Repository
Open your terminal, navigate to your desired directory workspace, and run the git clone command:
```bash
git clone https://github.com/gsk-2026/python-api python-api-local
```

### 2. Navigate to the Project Root
```bash
cd python-api-local   # Navigate to the project root containing all microservice modules, including practice_expandtesting_api
```

### 3. Initialize your Virtual Environment
Create a localized Python environment (`.venv`) to isolate dependencies:
```bash
# Windows
python -m venv .venv
source .\venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

---

##  Project Structure
```text
practice_expandtesting_api/
├── .github/
├── config/              # Environment configurations and global URL settings
├── logs/                # Local test execution logs (Git ignored)
├── performance/         # Load, stress, and spike test configurations
│   └── locustfile.py
├── src/                 # Shared source code helpers, API clients, and utilities
├── tests/               # Core test workspace
│   ├── unit/            # Isolated internal logic and code coverage
│   ├── e2e/             # Complete multi-endpoint user workflows
│   │   └── test_e2e_lifecycle.py
│   ├── integration/     # Isolated component and endpoint-level tests
│   │   ├── test_authorization.py
│   │   ├── test_health_check.py
│   │   ├── test_notes_*.py
│   │   └── test_users_*.py
│   └── conftest.py      # Shared test fixtures and pytest hooks
├── pytest.ini           # Independent module test settings
└── requirements.txt     # Module-specific dependencies
```

---

##  Local Setup & Prerequisites

Before running the tests in this module, ensure you have activated your Python virtual environment from the project root.

### 1. Install Module Dependencies
Run the installation command from the repository root, targeting this specific module's configuration:
```bash
pip install -r practice_expandtesting_api/requirements.txt
```

### 2. Environment Configurations
Ensure your local configurations are set up. If this module relies on variables from the root `.env` file, ensure the following fields are defined:
* `API_BASE_URL=https://practice.expandtesting.com/notes/api` *(or your target environment URL)*

---

## Running Tests

Always execute your commands from the **`python-api` project root directory** to ensure proper workspace resolution.

### 1. Run the Entire Test Suite (Integration + E2E)
```bash
pytest practice_expandtesting_api
```

### 2. Run Only Integration Tests
```bash
pytest practice_expandtesting_api/tests/integration
```

### 3. Run Only End-to-End (E2E) Lifecycle Tests
```bash
pytest practice_expandtesting_api/tests/e2e
```

### 4. Run a Specific Test File (Example)
```bash
pytest practice_expandtesting_api/tests/integration/test_health_check.py
```

### 5. Run Performance Tests
Spin up the performance UI from the terminal root:
```bash 
PYTHONPATH=practice_expandtesting_api locust -f practice_expandtesting_api/performance/locustfile.py
```
```bash 
PYTHONPATH=practice_expandtesting_api locust -f practice_expandtesting_api/performance/locustfile.py --headless -u 3 -r 1 -t 5m
```

---

## Test Logs
All test logs generated by Python's `logging` module during execution are captured locally within this folder at:
`practice_expandtesting_api/logs/pytest.log`

*Note: The `logs/` directory is automatically ignored by Git to prevent committing local environment test run artifacts.*

---


## CI/CD Pipelines

This repository supports flexible automated execution using both **GitHub Actions** and **Jenkins**.

### Pipeline Trigger Options

- **On-Demand / Manual Triggers:** Can be triggered manually at any time via `workflow_dispatch` in **GitHub Actions** or **Jenkins ("Build with Parameters")**.
- **Automated Code Events:** Runs automatically on push request events to key branch `main`.
- **Scheduled Runs:** Automated cron schedules can be configured in **Jenkins**.
- **Test Run Results:** Emailed out to specified Actions secrets and variables from **GitHub**.


### GitHub Actions Pipeline

The GitHub Actions workflow manages manual on-demand executions and automated test runs on git events.

#### Workflow Features & Controls
- **Flexible Scope Control (`TEST_SUITE_SCOPE`):** Execute `all`, `integration`, `e2e`, or `performance` test suites.
- **Dynamic Target Environments (`TEST_SUITE_ENV`):** Seamlessly run tests against `DFT`, `DIT`, `SIT`, or `UAT`.
- **Standalone HTML Reporting:** Automatically generates and archives HTML reports for Pytest and Locust.
- **Fault-Tolerant Execution:** Configured with `|| true` to ensure HTML reports are generated and uploaded even when tests fail.

#### Local Terminal Trigger Equivalents

```bash
# Integration Tests
pytest tests/integration/ --test_env SIT --html=output_reports/integration_report.html --self-contained-html

# End-to-End Tests
pytest tests/e2e/ --test_env SIT --html=output_reports/e2e_report.html --self-contained-html

# Locust Performance Tests
TEST_ENV=SIT locust -f performance/locustfile.py --config=performance/locust.conf --headless -u 3 -r 1 -t 5m --html output_reports/performance_report.html
```

---