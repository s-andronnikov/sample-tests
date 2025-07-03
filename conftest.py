import pytest
from playwright.sync_api import sync_playwright
import asyncio
import pytest
import pytest_asyncio
from playwright.async_api import async_playwright

from framework.ui.driver import Driver

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def browser_fixture():
    """Initialize browser for tests"""
    pw = await async_playwright().start()

    # Initialize the browser
    await Driver.init_browser(pw.chromium)
    # Create a new context
    await Driver.new_workspace()

    yield

    # Cleanup
    await Driver.close_contexts()
    await Driver.close_browser()
    await pw.stop()
from framework.ui.driver import Driver


@pytest_asyncio.fixture(scope="session")
async def start_session():
    async with async_playwright() as pw:
    # with sync_playwright() as pw:
        await Driver.init_browser(pw.chromium)
        yield
        await Driver.close_browser()


@pytest_asyncio.fixture(autouse=True)
async def launch_workspace(start_session):
    await Driver.new_workspace()
    yield
    await Driver.close_contexts()
