from enum import Enum, auto

from common.decorators import ui_url
from common.routes import UIRoutes
from config import base_settings
from framework.ui.element import By, Element
from ui.pages.base_page import BasePage


class UserType(Enum):
    """Available user types for login"""

    ADMIN = auto()
    USER = auto()
    READONLY = auto()


@ui_url(UIRoutes.LOGIN)
class LoginPage(BasePage):
    el_login = Element(By.LOCATOR, "input[name='emailAddress']")
    el_password = Element(By.LOCATOR, "input[name='password']")
    el_login_btn = Element(By.LOCATOR, "button[id='st-loginButton']")
    el_user_menu = Element(By.LOCATOR, "[role='listbox']:has(div:has-text('Settings'))")  # Settings dropdown menu
    el_logout = Element(By.LOCATOR, "div[name='logout'][role='option']", el_user_menu)

    error_toast = Element(By.LOCATOR, ".Toastify__toast--error")

    def login(self, login: str, password: str, check_already_logged_in: bool = True):
        """Login with the specified credentials

        Args:
            login: Username or email
            password: User password
            check_already_logged_in: If True, will check if already logged in and skip login if so

        Returns:
            Self for method chaining
        """
        if check_already_logged_in and self.is_user_logged_in():
            print("User is already logged in, skipping login")
            return self

        # If a user is logged in but we explicitly want to login as a different user
        if not check_already_logged_in and self.is_user_logged_in():
            self.logout()

        self.el_login.fill(login)
        self.el_password.fill(password)
        self.el_login_btn.click()

        # Wait for redirect to complete
        # self.should_be_redirected_from_login()
        return self

    def login_as(self, user_type: UserType, check_already_logged_in: bool = True):
        """Login with credentials based on user type

        Args:
            user_type: Type of user to login as (admin, regular user, readonly)
            check_already_logged_in: If True, will check if already logged in and skip login if so

        Returns:
            Self for method chaining
        """
        credentials = {
            UserType.ADMIN: (base_settings.admin_username, base_settings.admin_password),
            UserType.USER: (base_settings.user_username, base_settings.user_password),
            UserType.READONLY: (base_settings.readonly_username, base_settings.readonly_password),
        }
        username, password = credentials[user_type]
        return self.login(username, password, check_already_logged_in)

    def is_user_logged_in(self) -> bool:
        """Check if any user is currently logged in

        Returns:
            True if a user is logged in, False otherwise
        """
        return self.el_user_menu.is_visible()

    def open_user_menu(self):
        """Open the user menu dropdown to expose logout option

        Returns:
            Self for method chaining
        """
        self.el_user_menu.click()

        return self

    def logout(self):
        """Logout the current user if logged in

        Returns:
            Self for method chaining
        """
        if self.is_user_logged_in():
            # Open the user menu to expose the logout option
            self.open_user_menu()

            # Click on logout option
            self.el_logout.click()

            # Wait for logout to complete and login page to appear
            self.el_login.should_be_visible(timeout=5000)
        return self

    def should_see_error_toast(self, expected_message):
        self.error_toast.should_be_visible()
        message_span = self.error_toast.get_child_locator('span:has-text("' + expected_message + '")')

        assert message_span.should_be_visible(), f"Error toast with message '{expected_message}' not found"

    def should_be_redirected_from_login(self):
        """Verify that login redirection was successful by checking for the logout option

        Raises:
            AssertionError: If the logout element is not found after redirection

        Returns:
            Self for method chaining
        """
        # Wait for page load to complete
        assert self.el_user_menu.should_be_visible(timeout=5000), "User is not logged in - logout element not found after redirection"

        return self
