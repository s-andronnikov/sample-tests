import pytest

from ui.pages.tax_depreciation.asset_class_page import AssetClassPage
from ui.pages.tax_depreciation.basis_adjustment_page import BasisAdjustmentPage
from ui.pages.tax_depreciation.bonus_profile_page import BonusProfilePage
from ui.pages.contact_page import ContactPage
from ui.pages.login_page import LoginPage
from ui.pages.user_page import UserPage
from ui.pages.login_page import UserType
from ui.pages.tax_depreciation.depreciation_profile_page import DepreciationProfilePage


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


@pytest.fixture(scope="class")
def asset_class_page() -> AssetClassPage:
    """Return an AssetClassPage instance"""
    return AssetClassPage()


@pytest.fixture(scope="class")
def basis_adjustment_page():
    """Return a BasisAdjustmentPage instance"""
    return BasisAdjustmentPage()


@pytest.fixture
def authenticated_user_page(login_page, user_page) -> UserPage:
    """Return a UserPage instance with authenticated admin user"""
    # Authenticate as admin
    login_page.open()
    login_page.login_as(UserType.ADMIN, check_already_logged_in=True)
    # Open the user page
    user_page.open()
    return user_page


@pytest.fixture(scope="class")
def authenticated_asset_class_page(login_page, asset_class_page) -> AssetClassPage:
    """Return an AssetClassPage instance with authenticated admin user"""
    # Open login page and authenticate as admin
    login_page.open()
    login_page.login_as(UserType.ADMIN, check_already_logged_in=True)
    login_page.should_be_redirected_from_login()
    return asset_class_page


@pytest.fixture(scope="class")
def authenticated_basis_adjustment_page(login_page, basis_adjustment_page) -> BasisAdjustmentPage:
    """Return a BasisAdjustmentPage instance with authenticated admin user"""
    # Open login page and authenticate as admin
    login_page.open()
    login_page.login_as(UserType.ADMIN, check_already_logged_in=True)
    login_page.should_be_redirected_from_login()
    return basis_adjustment_page


@pytest.fixture(scope="class")
def bonus_profile_page() -> BonusProfilePage:
    """Return an AssetClassPage instance"""
    return BonusProfilePage()


@pytest.fixture(scope="class")
def authenticated_bonus_profile_page(login_page, bonus_profile_page) -> BonusProfilePage:
    login_page.open()
    login_page.login_as(UserType.ADMIN, check_already_logged_in=True)
    login_page.should_be_redirected_from_login()

    return BonusProfilePage()


@pytest.fixture(scope="class")
def depreciation_profile_page() -> DepreciationProfilePage:
    return DepreciationProfilePage()


@pytest.fixture(scope="class")
def authenticated_depreciation_profile_page(login_page, depreciation_profile_page) -> DepreciationProfilePage:
    login_page.open()
    login_page.login_as(UserType.ADMIN, check_already_logged_in=True)
    login_page.should_be_redirected_from_login()

    return depreciation_profile_page


@pytest.fixture
def authenticated_contact_page(login_page, contact_page) -> ContactPage:
    """Return a ContactPage instance with authenticated admin user"""
    # Authenticate as admin
    login_page.open()
    login_page.login_as(UserType.ADMIN, check_already_logged_in=True)

    # Open the contact page
    contact_page.open()
    return contact_page
