# Practice ExpandTesting API Automation Module

This is an independent, self-contained API testing microservice framework built to validate the endpoints provided by the ExpandTesting practice platform.  The purpose of this testing module is to ensure the functional health, schema reliability, and security contracts of the production REST APIs hosted on the **[ExpandTesting Practice Portal](https://expandtesting.com)**, **[Notes API Documentation](https://practice.expandtesting.com/notes/api/api-docs/#/)**.

As a dedicated QA exercise application, the application simulates realistic, multi-tiered technical environments. This test automation suite targets critical microservice subsets across integration, end-to-end, and performance layers:
* **User Authentication & Session Tokens:** Verifying user registration, login, logout, profile updates, password modification, and account deletion workflows.
* **Core Business Logic (Notes Application):** Programmatically asserting database persistence contracts—specifically verifying CRUD operations (POST, GET, PUT, PATCH, DELETE) for the notes service.
* **System Stability & Authorization:** Validating token filters (Authorize apiKey) and component-level baseline health checks (/health-check)
---


##  Module Microservic Structure
```text
practice_expandtesting_api/
├── config/              
│   └── __init__.py
│   └── settings.py
├── logs/                
├── performance/         
│   └── locust.conf
│   └── locustfile.py
├── src/                 
├── tests/               
│   ├── e2e/             
│   │   └── test_e2e_lifecycle.py
│   ├── integration/     
│   │   ├── test_authorization.py
│   │   ├── test_health_check.py
│   │   ├── test_notes_*.py
│   │   └── test_users_*.py
│   └── conftest.py      
├── conftest.py          
├── pytest.ini           
├── README.md            
├── requirements.txt     
└── practice_expandtesting_api.iml
```

---

##  Getting Started & Source Code Download

### 1. Clone the Repository
```bash
git clone https://github.com/gsk-2026/python-api python-api-local
```

### 2. Navigate to the Project Root
```bash
cd python-api-local   
```

### 3. Initialize Virtual Environment
```bash
# Windows
python -m venv .venv
source .\venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

---


##  Local Setup & Prerequisites

### 1. Install Module Dependencies

```bash
pip install -r practice_expandtesting_api/requirements.txt
```

### 2. Environment Configurations
* Ensure your local specific configurations are set up from the root `.env` file. Example:
* `API_BASE_URL=https://practice.expandtesting.com/notes/api` *(or your target environment URL)*

---

## Running Tests

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

### 4. Run a Specific Test File 
```bash
pytest practice_expandtesting_api/tests/integration/test_health_check.py
```

### 5. Run Performance Tests 
```bash 
PYTHONPATH=practice_expandtesting_api locust -f practice_expandtesting_api/performance/locustfile_practice_expandtesting.py
```
```bash 
PYTHONPATH=practice_expandtesting_api locust -f practice_expandtesting_api/performance/locustfile_practice_expandtesting.py --headless -u 3 -r 1 -t 5m --console-stats-interval 15
```
```bash 
PYTHONPATH=practice_expandtesting_api locust -f practice_expandtesting_api/performance/locustfile_practice_expandtesting.py,practice_expandtesting_api/performance/scenarios/smoke.py --headless --console-stats-interval 5
```
```bash 
PYTHONPATH=practice_expandtesting_api locust -f practice_expandtesting_api/performance/locustfile_practice_expandtesting.py,practice_expandtesting_api/performance/scenarios/load.py --headless --console-stats-interval 5
```
```bash 
PYTHONPATH=practice_expandtesting_api locust -f practice_expandtesting_api/performance/locustfile_practice_expandtesting.py,practice_expandtesting_api/performance/scenarios/stress.py --headless --console-stats-interval 5
```
```bash 
PYTHONPATH=practice_expandtesting_api locust -f practice_expandtesting_api/performance/locustfile_practice_expandtesting.py,practice_expandtesting_api/performance/scenarios/spike.py --headless --console-stats-interval 5
```

---

## Test Logs
*Note: The `logs/` directory is automatically ignored by Git to prevent committing local environment test run artifacts.*

`practice_expandtesting_api/logs/pytest.log`

---


## CI/CD Pipelines

### Jenkins Pipeline Trigger Options

- **On-Demand / Manual Triggers:** Can be triggered manually at any time via  **Jenkins** ("Build with Parameters").
- **Scheduled Runs:** Automated cron schedules are configured in **Jenkins** pipeline

### GitHub Actions Pipeline

- The **GitHub Actions** workflow manages manual on-demand executions.
- Every commit pushed to **GitHub** repository main will trigger 'all' test suite for environment 'DIT' 

#### Workflow Features & Controls
- **Flexible Scope Control (`TEST_SUITE_SCOPE`):** Execute `all`, `integration`, `e2e`, or `performance` test suites.
- **Dynamic Target Environments (`TEST_SUITE_ENV`):** Run tests seamlessly across `DIT`, `SIT`, or `UAT`.
- **Standalone HTML Reporting:** Generate and archive HTML reports for Pytest and Locust.
- **Test Reporting Email Notification:** Send test reports directly to recipients configured via GitHub repo secrets

### Local Terminal Trigger Equivalents (Example)

```bash
# Integration Tests
pytest tests/integration/ --test_env SIT --html=output_reports/integration_report.html --self-contained-html

# End-to-End Tests
pytest tests/e2e/ --test_env SIT --html=output_reports/e2e_report.html --self-contained-html

# Locust Performance Tests
TEST_ENV=SIT locust -f performance/locustfile_practice_expandtesting.py --config=performance/locust_practice_expandtesting.conf --headless -u 3 -r 1 -t 5m --html output_reports/performance_report.html
```

---