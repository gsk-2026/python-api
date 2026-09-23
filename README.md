# Python API Automation Framework (Monorepo Root)

Welcome to the **python-api** testing repository. This project is structured as a consolidated monorepo designed to house multiple independent, isolated API testing microservices. Each subdirectory operates as a standalone test suite with its own separate requirements, configuration files, and testing boundaries.

---

##  Repository Architecture & Ecosystem

While all testing suites share the same root Git repository and global virtual environment, **no module depends on another**. They are completely sandboxed to prevent dependency collisions and code cross-pollination.

```text
python-api/
│
├── .idea/                             # IntelliJ / PyCharm project configuration files
├── .gitignore                         # Global repo-level exclusions
├── README.md                          # Global repository orchestration manual
├── requirements.txt                   # Global core dependencies (Shared framework engines)
├── .env                               # Global baseline environment values (Shared)
├── .venv/                             # Unified workspace virtual environment
│
├── practice_expandtesting_api/       # Independent Testing Module 1
│   ├── config/
│   ├── performance/
│   ├── src/
│   ├── tests/
│   ├── pytest.ini                     # Local module configurations
│   ├── requirements.txt               # Local module dependency manifest
│   └── README.md                      # Module-specific onboarding manual
│
└── [new_microservice_api]/         # Independent Testing Module 2 (e.g., a_api, b_api)
    ├── pytest.ini
    └── requirements.txt
```

---

## Getting Started & Global Setup

Follow these steps to clone the code, configure your global workspace environment, and initialize package dependency controls.

### 1. Clone the Codebase
Open your terminal workspace and execute the git clone operation:
```bash
git clone https://github.com/gsk-2026/python-api python-api-local
cd python-api-local
```

### 2. Configure the Python Virtual Environment
Initialize and activate your isolated Python environment from the project root:
```bash
# Windows (Git Bash/ CMD / PowerShell)
python -m venv .venv
source .venv/Scripts/activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Project Dependencies 
Install manifest file
```bash
pip install -r requirements.txt
```

---

## Cross-Module Test Execution

All runtime execution triggers must be dispatched from the **`python-api` project root** folder to ensure clean, deterministic path resolution.

### Module 1: Practice ExpandTesting API
To work out of the ExpandTesting microservice suite, install its respective manifest profile and fire tests selectively:

```bash
# Install specific module dependencies
pip install -r practice_expandtesting_api/requirements.txt

# Run the entire functional test suite (Unit, Integration, E2E)
pytest practice_expandtesting_api

# Run a localized test domain slice
pytest practice_expandtesting_api/tests/integration
pytest practice_expandtesting_api/tests/e2e

# Run Performance load test vectors (Locust)
PYTHONPATH=practice_expandtesting_api locust -f practice_expandtesting_api/performance/locustfile.py --web-port 8090
```

### Module 2: Future New Applications (e.g., `a_api`)
When scaling up or interacting with separate components, follow the identical structured sandbox pattern:
```bash
# Install local packages
pip install -r a_api/requirements.txt

# Run testing frameworks locally
pytest a_api
```

## Environmental Verification Matrix

| Target Microservice | Domain Purpose | Framework Engine | Module Status |
| :--- | :--- | :--- | :--- |
| `practice_expandtesting_api` | Practice Portal API Health Checks | Pytest & Locust | 🟢 Active |
| `a_api` / `b_api` | Scaled Business Testing Sub-systems | Pytest | 🟡 Planning |
