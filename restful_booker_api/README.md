# Restful Booker API Automation Suite

This is an independent, self-contained API testing microservice framework built to validate the endpoints provided by the Restful Booker platform.  The purpose of this testing suite is to ensure the functional health, schema reliability, and security contracts of the production **[API playground created by Mark Winteringham](https://restful-booker.herokuapp.com/)**, **[Restful Booker API Documentation](https://restful-booker.herokuapp.com/apidoc/index.html)**.

---


##  Suite Microservic Structure
```text
restful_booker_api/
├── config/ 
│   └── settings.py
├── logs/                
├── performance/         
│   └── locust_restful_booker.conf
│   └── locustfile_restful_booker.py
├── src/                 
├── tests/               
│   ├── e2e/             
│   │   └── test_e2e_restful_booker.py
│   ├── integration/     
│   │   ├── test_auth_create_token.py 
│   │   ├── test_booking_*.py
│   │   └── test_ping_health_check.py
│   └── conftest.py       
├── pytest.ini           
├── README.md            
├── requirements.txt     
├── __init__.py          
└── restful_booker_api.iml
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

### 1. Install Suite Dependencies

```bash
pip install -r restful_booker_api/requirements.txt
```

### 2. Environment Configurations
* Ensure your local specific configurations are set up from the root `.env` file. Example:
* `API_BASE_URL=https://restful-booker.herokuapp.com` *(or your target environment URL)*

---

## Running Tests

### 1. Run the Entire Test Scope (Integration + E2E)
```bash
pytest restful_booker_api
```

### 2. Run Only Integration Tests
```bash
pytest restful_booker_api/tests/integration
```

### 3. Run Only End-to-End (E2E) Lifecycle Tests
```bash
pytest restful_booker_api/tests/e2e
```

### 4. Run a Specific Test File
```bash
pytest restful_booker_api/tests/integration/test_ping_health_check.py
```

### 5. Run Performance Tests
```bash 
PYTHONPATH=restful_booker_api locust -f restful_booker_api/performance/locustfile_restful_booker.py
```
```bash 
PYTHONPATH=restful_booker_api locust -f restful_booker_api/performance/locustfile_restful_booker.py --headless -u 3 -r 1 -t 5m --console-stats-interval 15
```

---

## Test Logs
*Note: The `logs/` directory is automatically ignored by Git to prevent committing local environment test run artifacts.*

`restful_booker_api/logs/pytest.log`

---


## CI/CD Pipelines

### Jenkins Pipeline Trigger Options

- **On-Demand / Manual Triggers:** Can be triggered manually at any time via  **Jenkins** ("Build with Parameters").
- **Scheduled Runs:** Automated cron schedules are configured in **Jenkins** pipeline

### GitHub Actions Pipeline

- The **GitHub Actions** workflow manages manual on-demand executions.
- Every commit pushed to **GitHub** repository main will trigger 'all' test scope for environment 'DIT'

#### Workflow Features & Controls
- **Flexible Scope Control (`GIT_TEST_SCOPE`):** Execute `all`, `integration`, `e2e`, or `performance` test scopes.
- **Dynamic Target Environments (`GIT_TEST_ENV`):** Run tests seamlessly across `DIT`, `SIT`, or `UAT`.
- **Standalone HTML Reporting:** Generate and archive HTML reports for Pytest and Locust.
- **Test Reporting Email Notification:** Send test reports directly to recipients configured via GitHub repo secrets

### Local Terminal Trigger Equivalents (Example)

```bash
# Move to the suite folder
cd restful_booker_api

# Integration Tests
TEST_ENV=SIT pytest tests/integration/ --html=output_reports/integration_report.html --self-contained-html

# End-to-End Tests
TEST_ENV=SIT pytest tests/e2e/ --html=output_reports/e2e_report.html --self-contained-html

# Locust Performance Tests
TEST_ENV=SIT locust -f performance/locustfile_restful_booker.py --config=performance/locust_restful_booker.conf --headless -u 3 -r 1 -t 5m --html output_reports/performance_report.html
```

---