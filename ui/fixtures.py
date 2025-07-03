import pytest

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
