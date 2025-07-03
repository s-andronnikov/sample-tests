from typing import Optional

from faker import Faker
from framework.ui.driver import Driver
from framework.ui.element import BaseElement, By
from framework.ui.list_elements import Grid
from config import base_settings

from ui.pages.components.contact_dialog import ContactDialog

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


@url("contacts")
class ContactPage(BasePage):
    """Contact page object"""

    def __init__(self):
        # Page elements
        self.title = BaseElement(By.LOCATOR, "h1")
        self.add_contact_btn = BaseElement(By.TEXT, "Add Contact")
        self.search_input = BaseElement(By.PLACEHOLDER, "Search contacts...")
        self.search_btn = BaseElement(By.LOCATOR, "button.search-button")

        # Contact grid
        self.grid = Grid()

        # Alert for notifications
        self.alert = BaseElement(By.LOCATOR, ".alert")

        # Contact dialog component
        self.contact_dialog = ContactDialog()

    def add_contact(self, 
                    first_name: str = None, 
                    last_name: str = None, 
                    email: str = None, 
                    phone: str = None, 
                    address: str = None, 
                    notes: str = None, 
                    user_id: str = None):
        """Add a new contact"""
        # Generate random data if not provided
        first_name = first_name or fake.first_name()
        last_name = last_name or fake.last_name()
        email = email or fake.email()
        phone = phone or fake.phone_number()
        address = address or fake.address()
        notes = notes or fake.text(max_nb_chars=100)

        # Click add contact button
        self.add_contact_btn.click()

        # Wait for dialog to appear
        self.contact_dialog.should_be_visible()

        # Fill the form and save
        self.contact_dialog.fill_form(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            notes=notes,
            user_id=user_id
        ).save()

        return self

    def search_contact(self, search_term: str):
        """Search for a contact"""
        self.search_input.fill(search_term)
        self.search_btn.click()
        return self

    def get_contact_row(self, name: str):
        """Find a contact row by name"""
        return self.grid.find_row_by_text(name)

    def edit_contact(self, name: str, **kwargs):
        """Edit a contact"""
        # Find the contact row
        contact_row = self.get_contact_row(name)
        if contact_row is None:
            raise ValueError(f"Contact with name '{name}' not found")

        # Click the edit button in the row
        edit_button = BaseElement(By.TEXT, "Edit", contact_row.locator)
        edit_button.click()

        # Wait for dialog to appear and fill the form
        self.contact_dialog.should_be_visible()
        self.contact_dialog.fill_form(**kwargs).save()

        return self

    def delete_contact(self, name: str):
        """Delete a contact"""
        # Find the contact row
        contact_row = self.get_contact_row(name)
        if contact_row is None:
            raise ValueError(f"Contact with name '{name}' not found")

        # Click the delete button in the row
        delete_button = BaseElement(By.TEXT, "Delete", contact_row.locator)
        delete_button.click()

        # Confirm deletion
        confirm_button = BaseElement(By.TEXT, "Confirm")
        confirm_button.click()

        return self

    def should_see_contact(self, name: str):
        """Assert that a contact is visible in the grid"""
        contact_row = self.get_contact_row(name)
        assert contact_row is not None, f"Contact '{name}' not found in the grid"
        return self

    def should_not_see_contact(self, name: str):
        """Assert that a contact is not visible in the grid"""
        contact_row = self.get_contact_row(name)
        assert contact_row is None, f"Contact '{name}' found in the grid but should not be present"
        return self

    def view_contact_details(self, name: str):
        """View contact details"""
        # Find the contact row
        contact_row = self.get_contact_row(name)
        if contact_row is None:
            raise ValueError(f"Contact with name '{name}' not found")

        # Click the view button in the row
        view_button = BaseElement(By.TEXT, "View", contact_row.locator)
        view_button.click()

        return self
