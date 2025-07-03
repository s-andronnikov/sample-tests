import pytest
from playwright.sync_api import sync_playwright

from framework.ui.driver import Driver


@pytest.fixture(scope="session")
def start_session():
    with sync_playwright() as pw:
        Driver.init_browser(pw.chromium)
        yield
        Driver.close_browser()


@pytest.fixture(autouse=True)
def launch_workspace(start_session):
    Driver.new_workspace()
    yield
    Driver.close_contexts()
