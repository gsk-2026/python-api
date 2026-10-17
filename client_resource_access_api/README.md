# Client Resource Access API Automation Suite

This is an independent, self-contained API testing microservice framework built to validate the endpoints developed by **[API playground created by Sankui Gou](https://github.com/gsk-2026/java-api/tree/main/client-resource-access-api)**.


---


##  Suite Microservic Structure
```text
client_resource_access_api/
├── config/              
│   └── __init__.py
│   └── settings.py
├── helper/              
│   └── lifecycle.py
├── data/              
│   └── client-resource-access-api.json
│   └── client-resource-access-api-0.0.1-SNAPSHOT.jar
├── logs/                
├── performance/         
│   └── locust.conf
│   └── locustfile.py
├── src/                 
├── tests/               
│   ├── e2e/             
│   │   └── test_e2e_lifecycle.py
│   ├── integration/     
│   │   ├── test_client_*.py
│   │   ├── test_resource_*.py 
│   │   └── test_client_resource_access_*.py
│   └── conftest.py      
├── conftest.py          
├── pytest.ini           
├── README.md            
├── requirements.txt     
└── client_resource_access_api.iml
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
pip install -r client_resource_access_api/requirements.txt
```

### 2. Environment Configurations
* Ensure your local specific configurations are set up from the root `.env` file. Example:
* `API_BASE_URL=http://localhost:8181` *(or your target environment URL)*

---

## Running Tests

### 1. Run the Entire Test Scope (Integration + E2E)
```bash
pytest client_resource_access_api
```

### 2. Run Only Integration Tests
```bash
pytest client_resource_access_api/tests/integration
```

### 3. Run Only End-to-End (E2E) Lifecycle Tests
```bash
pytest client_resource_access_api/tests/e2e
```

### 4. Run a Specific Test File
```bash
pytest client_resource_access_api/tests/integration/test_client_post.py
```

### 5. Run Performance Tests
```bash 
PYTHONPATH=client_resource_access_api locust -f client_resource_access_api/performance/locustfile_client_resource_access.py
```
```bash 
PYTHONPATH=client_resource_access_api locust -f client_resource_access_api/performance/locustfile_client_resource_access.py --headless -u 3 -r 1 -t 5m --console-stats-interval 15
```

---

## Test Logs
*Note: The `logs/` directory is automatically ignored by Git to prevent committing local environment test run artifacts.*

`client_resource_access_api/logs/pytest.log`

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
cd client_resource_access_api

# Integration Tests
pytest tests/integration/ --test_env SIT --html=output_reports/integration_report.html --self-contained-html

# End-to-End Tests
pytest tests/e2e/ --test_env SIT --html=output_reports/e2e_report.html --self-contained-html

# Locust Performance Tests
TEST_ENV=SIT locust -f performance/locustfile_client_resource_access.py --config=performance/locust_client_resource_access.conf --headless -u 3 -r 1 -t 5m --html output_reports/performance_report.html
```

---