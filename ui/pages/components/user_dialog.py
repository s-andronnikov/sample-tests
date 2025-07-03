from typing import Optional

from framework.ui.element import BaseElement, By


class UserDialog:
    """User dialog component for adding/editing users"""

    def __init__(self, parent: Optional[BaseElement] = None):
        self.parent = parent

        # Dialog elements
        self.dialog = BaseElement(By.LOCATOR, ".user-dialog", parent)
        self.title = BaseElement(By.LOCATOR, ".dialog-title", self.dialog)

        # Form inputs
        self.username_input = BaseElement(By.LOCATOR, "input[name='username']", self.dialog)
        self.email_input = BaseElement(By.LOCATOR, "input[name='email']", self.dialog)
        self.first_name_input = BaseElement(By.LOCATOR, "input[name='firstName']", self.dialog)
        self.last_name_input = BaseElement(By.LOCATOR, "input[name='lastName']", self.dialog)
        self.password_input = BaseElement(By.LOCATOR, "input[name='password']", self.dialog)
        self.phone_input = BaseElement(By.LOCATOR, "input[name='phone']", self.dialog)
        self.active_checkbox = BaseElement(By.LOCATOR, "input[name='isActive']", self.dialog)

        # Buttons
        self.save_button = BaseElement(By.TEXT, "Save", self.dialog)
        self.cancel_button = BaseElement(By.TEXT, "Cancel", self.dialog)

    def fill_form(self, 
                  username: Optional[str] = None,
                  email: Optional[str] = None,
                  first_name: Optional[str] = None,
                  last_name: Optional[str] = None,
                  password: Optional[str] = None,
                  phone: Optional[str] = None,
                  is_active: Optional[bool] = None):
        """Fill the user form"""
        if username is not None:
            self.username_input.fill(username)

        if email is not None:
            self.email_input.fill(email)

        if first_name is not None:
            self.first_name_input.fill(first_name)

        if last_name is not None:
            self.last_name_input.fill(last_name)

        if password is not None:
            self.password_input.fill(password)

        if phone is not None:
            self.phone_input.fill(phone)

        if is_active is not None:
            if is_active and not self.active_checkbox._get_locator().is_checked():
                self.active_checkbox.check()
            elif not is_active and self.active_checkbox._get_locator().is_checked():
                self.active_checkbox.uncheck()

        return self

    def save(self):
        """Click the save button"""
        self.save_button.click()
        return self

    def cancel(self):
        """Click the cancel button"""
        self.cancel_button.click()
        return self

    def should_be_visible(self):
        """Check if the dialog is visible"""
        self.dialog.should_be_visible()
        return self
