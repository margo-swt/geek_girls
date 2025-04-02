# Contact List Test Automation

This project contains automated tests for the Contact List application, focusing on user registration functionality with SQL database integration and API verification.

## Features

- Selenium WebDriver test automation
- SQL database integration for test data management
- API request verification
- Screenshot capture for test steps
- HTML test reports with embedded screenshots
- Configurable WebDriver settings
- Faker integration for test data generation

## Project Structure

```
├── config/
│   ├── webdriver_config.py    # WebDriver configuration
│   └── api_config.py          # API configuration
├── pages/
│   ├── add_user_page.py       # Add User page object
│   ├── contact_list_page.py   # Contact List page object
│   └── login_page.py          # Login page object
├── tests/
│   ├── base_test.py          # Base test class
│   └── test_sql_user_registration.py  # User registration tests
├── reports/
│   └── assets/
│       └── style.css         # Custom CSS for HTML reports
├── screenshots/              # Test execution screenshots
├── requirements.txt         # Project dependencies
└── README.md               # Project documentation
```

## Prerequisites

- Python 3.12 or higher
- Chrome browser
- ChromeDriver matching your Chrome version

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd geek_girls
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The project uses several configuration files:

- `config/webdriver_config.py`: Configure Chrome WebDriver settings
- `config/api_config.py`: Configure API endpoints and request settings
- `reports/assets/style.css`: Customize HTML report styling

## Running Tests

Run the user registration test with HTML report generation:

```bash
PYTHONPATH=$PYTHONPATH:. pytest tests/test_sql_user_registration.py -v --html=reports/report.html --css=reports/assets/style.css
```

### Test Features

1. **Database Integration**
   - Creates temporary SQLite database
   - Generates test users with Faker
   - Cleans up after test execution

2. **Screenshot Capture**
   - Takes screenshots at key test steps
   - Embeds screenshots in HTML report
   - Maintains timestamped screenshot history

3. **API Verification**
   - Verifies API responses
   - Handles duplicate email scenarios
   - Validates error messages

4. **HTML Reports**
   - Generates detailed test reports
   - Includes embedded screenshots
   - Custom styling for better readability

## Project Structure Details

### Page Objects

- `AddUserPage`: Handles user registration form interactions
- `ContactListPage`: Manages contact list view functionality
- `LoginPage`: Handles login form interactions

### Configuration

- `WebDriverConfig`: Manages Chrome WebDriver setup
- `APIConfig`: Handles API request configuration

### Test Files

- `base_test.py`: Contains common test setup and teardown
- `test_sql_user_registration.py`: User registration test cases

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 