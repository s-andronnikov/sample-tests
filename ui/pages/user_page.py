from typing import Optional

from faker import Faker

from config import base_settings
from framework.ui.driver import Driver
from framework.ui.element import BaseElement, By
from framework.ui.list_elements import Grid

from ui.pages.components.user_dialog import UserDialog

# Initialize Faker
fake = Faker()


def url(_url: str = None):
    """Decorator for setting page URL"""
    def inner(page_class):
        page_class.url = f"https://{base_settings.host}/{_url or ''}"
        return page_class
    return inner


class BasePage:
    """Base class for all pages"""
    url: str = None

    def open(self):
        """Open the page"""
        Driver.goto(self.url)
        return self


@url("users")
class UserPage(BasePage):
    """User page object"""

    def __init__(self):
        # Page elements
        self.title = BaseElement(By.LOCATOR, "h1")
        self.add_user_btn = BaseElement(By.TEXT, "Add User")
        self.search_input = BaseElement(By.PLACEHOLDER, "Search users...")
        self.search_btn = BaseElement(By.LOCATOR, "button.search-button")

        # User grid
        self.grid = Grid()

        # Alert for notifications
        self.alert = BaseElement(By.LOCATOR, ".alert")

        # User dialog component
        self.user_dialog = UserDialog()

        # Login form elements
        self.login_input = BaseElement(By.LOCATOR, "input[name='login']")
        self.password_input = BaseElement(By.LOCATOR, "input[name='password']")
        self.login_btn = BaseElement(By.TEXT, "Login")

    def login(self, username: str, password: str):
        """Login with the provided credentials"""
        self.login_input.fill(username)
        self.password_input.fill(password)
        self.login_btn.click()
        return self

    def add_user(self, 
                 username: str = None, 
                 email: str = None, 
                 first_name: str = None, 
                 last_name: str = None, 
                 password: str = None, 
                 phone: str = None):
        """Add a new user"""
        # Generate random data if not provided
        username = username or fake.user_name()
        email = email or fake.email()
        first_name = first_name or fake.first_name()
        last_name = last_name or fake.last_name()
        password = password or fake.password()
        phone = phone or fake.phone_number()

        # Click add user button
        self.add_user_btn.click()

        # Wait for dialog to appear
        self.user_dialog.should_be_visible()

        # Fill the form and save
        self.user_dialog.fill_form(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            phone=phone,
            is_active=True
        ).save()

        return self

    def search_user(self, search_term: str):
        """Search for a user"""
        self.search_input.fill(search_term)
        self.search_btn.click()
        return self

    def get_user_row(self, username: str):
        """Find a user row by username"""
        return self.grid.find_row_by_text(username)

    def edit_user(self, username: str, **kwargs):
        """Edit a user"""
        # Find the user row
        user_row = self.get_user_row(username)
        if user_row is None:
            raise ValueError(f"User with username '{username}' not found")

        # Click the edit button in the row
        edit_button = BaseElement(By.TEXT, "Edit", user_row.locator)
        edit_button.click()

        # Wait for dialog to appear and fill the form
        self.user_dialog.should_be_visible()
        self.user_dialog.fill_form(**kwargs).save()

        return self

    def delete_user(self, username: str):
        """Delete a user"""
        # Find the user row
        user_row = self.get_user_row(username)
        if user_row is None:
            raise ValueError(f"User with username '{username}' not found")

        # Click the delete button in the row
        delete_button = BaseElement(By.TEXT, "Delete", user_row.locator)
        delete_button.click()

        # Confirm deletion
        confirm_button = BaseElement(By.TEXT, "Confirm")
        confirm_button.click()

        return self

    def should_see_user(self, username: str):
        """Assert that a user is visible in the grid"""
        user_row = self.get_user_row(username)
        assert user_row is not None, f"User '{username}' not found in the grid"
        return self

    def should_not_see_user(self, username: str):
        """Assert that a user is not visible in the grid"""
        user_row = self.get_user_row(username)
        assert user_row is None, f"User '{username}' found in the grid but should not be present"
        return self
