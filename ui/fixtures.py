import pytest

from config import base_settings
from ui.pages.asset_class_page import AssetClassPage
from ui.pages.contact_page import ContactPage
from ui.pages.login_page import LoginPage
from ui.pages.user_page import UserPage


@pytest.fixture
def login_page() -> LoginPage:
    return LoginPage()


@pytest.fixture
def user_page() -> UserPage:
    """Return a UserPage instance"""
    return UserPage()


@pytest.fixture
def contact_page() -> ContactPage:
    """Return a ContactPage instance"""
    return ContactPage()


@pytest.fixture
def asset_class_page() -> AssetClassPage:
    """Return an AssetClassPage instance"""
    return AssetClassPage()

@pytest.fixture
def authenticated_asset_class_page(login_page, asset_class_page) -> AssetClassPage:
    """Return a UserPage instance with authenticated user"""
    login_page.open()
    login_page.login(base_settings.admin_username, base_settings.admin_password)
    login_page.should_be_redirected_from_login()

    return asset_class_page


@pytest.fixture
def authenticated_user_page(user_page) -> UserPage:
    """Return a UserPage instance with authenticated user"""
    user_page.open()
    user_page.login("admin", "adminpassword")
    return user_page


@pytest.fixture
def authenticated_contact_page(contact_page, authenticated_user_page) -> ContactPage:
    """Return a ContactPage instance with authenticated user"""
    contact_page.open()
    return contact_page
