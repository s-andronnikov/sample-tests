from typing import Optional

from framework.ui.element import BaseElement, By


class ContactDialog:
    """Contact dialog component for adding/editing contacts"""

    def __init__(self, parent: Optional[BaseElement] = None):
        self.parent = parent

        # Dialog elements
        self.dialog = BaseElement(By.LOCATOR, ".contact-dialog", parent)
        self.title = BaseElement(By.LOCATOR, ".dialog-title", self.dialog)

        # Form inputs
        self.first_name_input = BaseElement(By.LOCATOR, "input[name='firstName']", self.dialog)
        self.last_name_input = BaseElement(By.LOCATOR, "input[name='lastName']", self.dialog)
        self.email_input = BaseElement(By.LOCATOR, "input[name='email']", self.dialog)
        self.phone_input = BaseElement(By.LOCATOR, "input[name='phone']", self.dialog)
        self.address_input = BaseElement(By.LOCATOR, "textarea[name='address']", self.dialog)
        self.notes_input = BaseElement(By.LOCATOR, "textarea[name='notes']", self.dialog)
        self.user_select = BaseElement(By.LOCATOR, "select[name='userId']", self.dialog)

        # Buttons
        self.save_button = BaseElement(By.TEXT, "Save", self.dialog)
        self.cancel_button = BaseElement(By.TEXT, "Cancel", self.dialog)

    def fill_form(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        notes: Optional[str] = None,
        user_id: Optional[str] = None,
    ):
        """Fill the contact form"""
        if first_name is not None:
            self.first_name_input.fill(first_name)

        if last_name is not None:
            self.last_name_input.fill(last_name)

        if email is not None:
            self.email_input.fill(email)

        if phone is not None:
            self.phone_input.fill(phone)

        if address is not None:
            self.address_input.fill(address)

        if notes is not None:
            self.notes_input.fill(notes)

        if user_id is not None:
            # Select option by value
            self.user_select._get_locator().select_option(value=user_id)

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
