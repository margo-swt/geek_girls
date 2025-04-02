# Contact List App Test Automation

This project contains automated tests for the Contact List application's Add User functionality, focusing on form validation and API testing.

## Project Structure

```
├── config/
│   └── webdriver_config.py     # WebDriver configuration and setup
├── pages/
│   ├── base_page.py           # Base page with common methods
│   └── add_user_page.py       # Add User page object
├── tests/
│   ├── conftest.py            # Test fixtures and configuration
│   └── test_add_user.py       # Test cases
├── utils/
├── reports/                    # Test execution reports
├── logs/                       # Test execution logs
├── .env.example               # Environment variables template
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Test Cases

### UI Tests

#### Empty Fields Validation Test
- **File**: `tests/test_add_user.py`
- **Test**: `test_empty_fields_validation`
- **Description**: Validates the form's error handling when submitting empty fields
- **Steps**:
  1. Opens the Add User page
  2. Submits the form with empty fields
  3. Verifies error message is displayed
  4. Validates the exact error message text:
     ```
     "User validation failed: firstName: Path `firstName` is required., 
      lastName: Path `lastName` is required., 
      email: Email is invalid, 
      password: Path `password` is required."
     ```
- **Tags**: `@pytest.mark.ui`, `@pytest.mark.negative`

### API Tests

#### Empty Fields API Validation Test
- **File**: `tests/test_add_user.py`
- **Test**: `test_empty_fields_api`
- **Description**: Validates the API's error handling when sending empty fields
- **Steps**:
  1. Sends POST request to `/users` endpoint with empty fields
  2. Verifies 400 status code response
  3. Validates error response contains all required field validations:
     - firstName
     - lastName
     - email
     - password
- **Tags**: `@pytest.mark.api`, `@pytest.mark.negative`

## Test Data

The tests use fixtures defined in `conftest.py`:
- `empty_user_data`: Provides empty field data for negative testing
- `api_headers`: Provides necessary headers for API requests

## Running Tests

Run all tests:
```bash
pytest
```

Run specific test types:
```bash
pytest -m ui        # Run only UI tests
pytest -m api       # Run only API tests
pytest -m negative  # Run only negative tests
```

Run tests in parallel:
```bash
pytest -n auto
```

## Test Reports

HTML reports are generated in the `reports` directory after each test run. The reports include:
- Test execution summary
- Test case details
- Error messages and screenshots (for failures)
- Test execution time

## Features

- Page Object Model (POM) design pattern
- Selenium WebDriver for UI testing
- Pytest test framework
- API testing with requests library
- Parallel test execution
- HTML test reports
- Environment configuration
- Cross-browser support (Chrome)
- Headless mode support 