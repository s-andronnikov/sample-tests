import pytest
from typing import Generator

from playwright.sync_api import Page

from framework.ui.driver import Driver
from config import base_settings


@pytest.fixture
def page() -> Page:
    """Return the current page from the driver"""
    return Driver.get_driver()


@pytest.fixture
def new_page() -> Page:
    """Create and return a new page"""
    return Driver.new_page()


@pytest.fixture
def base_url() -> str:
    """Return the base URL for UI tests"""
    return f"https://{base_settings.host}"


@pytest.fixture
def navigate_to(base_url) -> Generator[callable, None, None]:
    """Fixture that returns a function to navigate to a specific path"""

    def _navigate_to(path: str = "") -> None:
        url = f"{base_url}/{path.lstrip('/')}"
        Driver.goto(url)

    yield _navigate_to
