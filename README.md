# Testing Framework

A comprehensive testing framework for both UI and API testing using Playwright, Pytest, and Pydantic.

## Project Structure

```
├── api/  # API tests
├── common/
│   ├── api_client.py        # Client for API interactions
│   ├── db_client.py         # Client for database interactions
│   ├── data_factory.py      # Data factory for test data generation
│   ├── utils.py             # Helper functions
│   ├── models.py            # Data models for validation/generation
│   └── routes.py            # Routes for API/UI
├── resources/               # Constants/scripts/SQL queries for tests
├── framework/
│   ├── ui/
│   │   ├── driver.py        # Playwright driver
│   │   ├── element.py       # Base element for page interactions
│   │   ├── list_elements.py # List elements for page interactions
│   │   └── fixtures.py      # Base fixtures
├── ui/
│   ├── pages/
│   │   ├── components/
│   │   │   ├── user_dialog.py
│   │   │   └── contact_dialog.py
│   │   ├── contact_page.py
│   │   └── user_page.py
│   ├── fixtures.py
│   └── tests/
│       ├── test_contacts.py # UI tests for contacts section
│       └── test_users.py    # UI tests for users section
```

## Setup

1. Install Poetry: `pip install poetry`
2. Install dependencies: `poetry install`
3. Configure environment variables in `.env` file
4. Install Playwright browsers: `poetry run playwright install`

## Running Tests

```bash
# Run all tests
poetry run pytest

# Run UI tests
poetry run pytest ui/

# Run API tests
poetry run pytest api/

# Run with specific markers
poetry run pytest -m smoke
```

## Architecture

### Driver and BaseElement

The framework uses a separation of concerns approach:

- **Driver**: Singleton class that manages browser initialization, context creation, and page navigation
- **BaseElement**: Abstraction over locators that encapsulates element interaction logic

### Page Object Pattern

UI tests use the Page Object pattern to separate test logic from page representation.

### Data Models

Pydantic models are used for data validation and generation, ensuring type safety.
