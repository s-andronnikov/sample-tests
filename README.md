# Testing Framework

A comprehensive testing framework for both UI and API testing using Playwright, Pytest, and Pydantic.

## Requirements

- Python 3.12 or higher

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

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Upgrade pip

```bash
pip install --upgrade pip
```

### 3. Install Dependencies

```bash
# Install Poetry
pip install poetry

# Install project dependencies
poetry install
```

### 4. Configure Environment

Configure environment variables in `.env` file

### 5. Install Playwright Browsers

```bash
poetry run playwright install
```

## Running Tests

```bash
# Run all tests
poetry run pytest

# Run UI tests
poetry run pytest ui/
# or using marker
poetry run pytest -m ui

# Run API tests
poetry run pytest api/
# or using marker
poetry run pytest -m api

# Run with specific markers
poetry run pytest -m smoke
```

You can also use the Makefile commands for running tests:

```bash
# Run all tests
make test

# Run UI tests only
make test-ui

# Run API tests only
make test-api
```

## Makefile Commands

The project includes a Makefile with useful commands for development:

```bash
# Show all available commands with descriptions
make help

# Run linting checks with pre-commit
make lint

# Format code with black and ruff
make format

# Clean up Python artifacts and cache
make clean

# Run all tests
make test

# Run only UI tests
make test-ui

# Run only API tests
make test-api

# Install all dependencies including dev tools
make install

# Update dependencies
make update
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
