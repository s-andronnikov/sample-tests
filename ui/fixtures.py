import pytest

from config import base_settings
from ui.pages.asset_class_page import AssetClassPage
from ui.pages.basis_adjustment_page import BasisAdjustmentPage
from ui.pages.contact_page import ContactPage
from ui.pages.login_page import LoginPage
from ui.pages.user_page import UserPage
from ui.pages.login_page import UserType


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
def asset_class_page() -> AssetClassPage:
    """Return an AssetClassPage instance"""
    return AssetClassPage()


@pytest.fixture(scope="session")
def basis_adjustment_page():
    """Return a BasisAdjustmentPage instance"""
    return BasisAdjustmentPage()


@pytest.fixture(scope="class")
def authenticated_asset_class_page(login_page, asset_class_page) -> AssetClassPage:
    """Return an AssetClassPage instance with authenticated admin user"""
    # Open login page and authenticate as admin
    login_page.open()
    login_page.login_as(UserType.ADMIN, check_already_logged_in=True)

    return asset_class_page


@pytest.fixture(scope="class")
def authenticated_basis_adjustment_page(login_page, basis_adjustment_page):
    """Return a BasisAdjustmentPage instance with authenticated admin user"""
    # Open login page and authenticate as admin
    login_page.open()
    login_page.login_as(UserType.ADMIN, check_already_logged_in=True)

    return basis_adjustment_page


@pytest.fixture
def authenticated_user_page(login_page, user_page) -> UserPage:
    """Return a UserPage instance with authenticated admin user"""
    # Authenticate as admin
    login_page.open()
    login_page.login_as(UserType.ADMIN, check_already_logged_in=True)

    # Open the user page
    user_page.open()
    return user_page


@pytest.fixture
def authenticated_contact_page(login_page, contact_page) -> ContactPage:
    """Return a ContactPage instance with authenticated admin user"""
    # Authenticate as admin
    login_page.open()
    login_page.login_as(UserType.ADMIN, check_already_logged_in=True)

    # Open the contact page
    contact_page.open()
    return contact_page
