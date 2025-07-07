import pytest_asyncio
import pytest
import pytest_asyncio

from ui.pages.asset_class_page import AssetClassPage
from ui.pages.login_page import LoginPage


@pytest_asyncio.fixture
async def login_page():
    """Return a login page instance"""
    return LoginPage()


@pytest_asyncio.fixture
async def asset_class_page():
    """Return an asset class page instance"""
    return AssetClassPage()


@pytest_asyncio.fixture
async def authenticated_asset_class_page(login_page):
    """Return an authenticated asset class page instance"""
    await login_page.open()
    await login_page.login("admin", "password")
    await login_page.should_be_redirected_from_login()

    return AssetClassPage()
from ui.pages.contact_page import ContactPage
from ui.pages.login_page import LoginPage
from ui.pages.user_page import UserPage

import pytest

from ui.pages.asset_class_page import AssetClassPage
from ui.pages.login_page import LoginPage


@pytest.fixture
def login_page():
    """Return a login page instance"""
    return LoginPage()


@pytest.fixture
def asset_class_page():
    """Return an asset class page instance"""
    return AssetClassPage()


@pytest.fixture
def authenticated_asset_class_page(login_page):
    """Return an authenticated asset class page instance"""
    login_page.open()
    login_page.login("admin", "password")
    login_page.should_be_redirected_from_login()

    return AssetClassPage()
@pytest_asyncio.fixture
def login_page(browser_fixture) -> LoginPage:
    return LoginPage()


@pytest_asyncio.fixture
def user_page(browser_fixture) -> UserPage:
    """Return a UserPage instance"""
    return UserPage()


@pytest_asyncio.fixture
def contact_page(browser_fixture) -> ContactPage:
    """Return a ContactPage instance"""
    return ContactPage()


@pytest_asyncio.fixture
async def authenticated_user_page(user_page) -> UserPage:
    """Return a UserPage instance with authenticated user"""
    await user_page.open()
    await user_page.login("admin", "adminpassword")
    return user_page


@pytest_asyncio.fixture
async def authenticated_contact_page(contact_page, authenticated_user_page) -> ContactPage:
    """Return a ContactPage instance with authenticated user"""
    await contact_page.open()
    return contact_page


@pytest_asyncio.fixture
async def authenticated_user_page(user_page) -> UserPage:
    """Return a UserPage instance with authenticated user"""
    await user_page.open()
    await user_page.login("admin", "adminpassword")
    return user_page


@pytest_asyncio.fixture
async def authenticated_contact_page(contact_page, authenticated_user_page) -> ContactPage:
    """Return a ContactPage instance with authenticated user"""
    await contact_page.open()
    return contact_page
