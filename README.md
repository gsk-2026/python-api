# Python API Automation Framework (Monorepo Root)

Welcome to the **python-api** testing monorepo, featuring integrated GitHub and Jenkins CI/CD pipeline. This repository houses multiple independent API testing microservices. Each subdirectory operates as a standalone test suite with its own separate requirements, configuration files, and testing boundaries.

---

##  Repository Architecture & Ecosystem

```text
python-api/
│
├── .idea/                             # IDE configuration settings
├── .gitignore                         # Project-wide Git exclusion rules
├── Jenkinsfile                        # CI/CD pipeline definition
├── README.md                          # Root repository documentation
├── requirements.txt                   # Core dependencies
├── .env                               # Shared environment values
├── .venv/                             # Python virtual environment
│
├── practice_expandtesting_api/        # API testing module
│   ├── config/
│   ├── performance/
│   ├── src/
│   ├── tests/
│   ├── pytest.ini                     # Module pytest configuration
│   ├── requirements.txt               # Module specific dependency
│   └── README.md                      # Module-specific documentation
│
└── [new_microservice_api]/            # New microservice API testing module template
    ├── pytest.ini
    └── requirements.txt
```

---

## Getting Started & Global Setup

From **python-api-local** project root folder: clone the repository, set up your global workspace, and initialize package.

### 1. Clone the Codebase

```bash
git clone https://github.com/gsk-2026/python-api python-api-local
cd python-api-local
```

### 2. Configure the Python Virtual Environment

```bash
# Windows (Git Bash/ CMD / PowerShell)
python -m venv .venv
source .venv/Scripts/activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python Packages

```bash
pip install -r requirements.txt
```

---

## Cross-Module Test Execution
Installs module specific Python packages and versions. For detailed steps, please refer to README.md of **individual module**

### Module 1: Practice ExpandTesting API

```bash
# Install specific module dependencies
pip install -r practice_expandtesting_api/requirements.txt

# Run the entire functional test suite (Integration, E2E, performance/load et al.)
pytest practice_expandtesting_api
```

### Module 2: Future New Applications (e.g., `a_api`)

```bash
# Install local packages
pip install -r a_api/requirements.txt

# Run testing frameworks locally
pytest a_api
```

## Environmental Verification Matrix

| Target Microservice | Domain Purpose | Framework Engine | Module Status |
| :--- | :--- | :--- | :--- |
| `practice_expandtesting_api` | practice.expandtesting.com/notes/api | Pytest & Locust | 🟢 Active |
| `a_api` / `b_api` | Scaled Business Testing Sub-systems | Pytest | 🟡 Planning |


---

## CI/CD Pipelines

This repository supports flexible automated execution using **Jenkins**, and also manually thru both **GitHub Actions** and **Jenkins**.

### Jenkins Pipeline Trigger Options

- **On-Demand / Manual Triggers:** Can be triggered manually at any time via  **Jenkins** ("Build with Parameters").
- **Scheduled Runs:** Automated cron schedules are configured in **Jenkins** pipeline 

### GitHub Actions Pipeline

- The **GitHub Actions** workflow manages manual on-demand executions.

### Local Terminal Trigger Equivalents

Please refer the specification from README of individual modules for details

---
