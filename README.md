# Selenium Web Test Framework

This is a Python-based Selenium Web test framework using pytest.

## Prerequisites

1. Python 3.8 or higher
2. pip (Python package installer)

## Installation

1. Clone the repository
2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env` and update the values:
```bash
cp .env.example .env
```

2. Update the following variables in `.env`:
```
BASE_URL=https://your-application-url.com
VALID_USER=your_test_user
VALID_PASSWORD=your_test_password
BROWSER_TYPE=chrome  # or firefox
HEADLESS=false
```

## Running Tests

### Basic Commands

1. Run all tests:
```bash
pytest
```

2. Run specific test file:
```bash
pytest tests/test_login.py
```

3. Run specific test:
```bash
pytest tests/test_login.py::TestLogin::test_successful_login
```

### Test Categories

1. Run smoke tests only:
```bash
pytest -m smoke
```

2. Run regression tests only:
```bash
pytest -m regression
```

3. Run critical tests only:
```bash
pytest -m critical
```

### Browser Options

1. Run tests with Chrome:
```bash
BROWSER_TYPE=chrome pytest
```

2. Run tests with Firefox:
```bash
BROWSER_TYPE=firefox pytest
```

3. Run tests in headless mode:
```bash
HEADLESS=true pytest
```

### Additional Options

1. Generate HTML report:
```bash
pytest --html=reports/report.html
```

2. Run tests in parallel:
```bash
pytest -n auto
```

3. Run tests with verbose output:
```bash
pytest -v
```

4. Run tests with detailed failure information:
```bash
pytest -vv
```

## Test Reports and Logs

- HTML reports are generated in the `reports` directory
- Test logs are stored in the `logs` directory
- Screenshots of failed tests are saved in the `screenshots` directory
- Downloaded files are stored in the `downloads` directory

## Project Structure

```
├── pages/                  # Page Object Models
├── tests/                  # Test files
├── utils/                  # Utility functions
├── reports/               # Test reports
├── logs/                  # Test logs
├── screenshots/           # Screenshots of failed tests
├── downloads/            # Downloaded files
├── .env                  # Environment variables
├── pytest.ini           # Pytest configuration
└── requirements.txt     # Project dependencies
```