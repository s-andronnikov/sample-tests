from framework.ui.element import Element, By, BaseElement
from random import randint


class BonusProfileDialog(BaseElement):
    """Dialog component for creating and editing bonus profiles"""

    # Locators for dialog elements
    form_container = Element(By.LOCATOR, ".modal")
    form_title = Element(By.LOCATOR, ".modal-title")
    name_input = Element(By.LOCATOR, "input[name='name']")
    bonus_calculation_method_dropdown = Element(By.LOCATOR, "div[data-name='bonusCalculationMethod']")
    bonus_percent_input = Element(By.LOCATOR, "input[name='bonusPercent']")
    create_button = Element(By.LOCATOR, "button:has-text('Create')")
    save_button = Element(By.LOCATOR, "button:has-text('Save')")
    cancel_button = Element(By.LOCATOR, "button:has-text('Cancel')")
    error_message = Element(By.LOCATOR, ".labeled-error")

    def __init__(self):
        super().__init__(By.LOCATOR, ".modal")

    def fill_form(self, name: str | None = None, bonus_calculation_method: str = "Standard", bonus_percent: float | None = None) -> str:
        """Fill the bonus profile creation form

        Args:
            name: Name for the bonus profile (random if not provided)
            bonus_calculation_method: Method for bonus calculation (Standard by default)
            bonus_percent: Bonus percent value (random if not provided)

        Returns:
            The name used for the bonus profile
        """
        # Generate random name if not provided
        if name is None:
            name = f"Test Bonus Profile {randint(1000, 9999)}"

        # Fill name field
        self.name_input.fill(name)

        # Select bonus calculation method
        self.bonus_calculation_method_dropdown.click()
        method_option = Element(By.LOCATOR, f".dropdown-item:has-text('{bonus_calculation_method}')")
        method_option.click()

        # Fill bonus percent
        if bonus_percent is None:
            bonus_percent = randint(10, 95)  # Random percent between 10% and 95%

        self.bonus_percent_input.fill(str(bonus_percent))

        return name

    def create(self):
        """Click the Create button to submit the form

        Returns:
            Self for method chaining
        """
        self.create_button.click()
        return self

    def save(self):
        """Click the Save button to submit the form

        Returns:
            Self for method chaining
        """
        self.save_button.click()
        return self

    def cancel(self):
        """Click the Cancel button to close the form without saving

        Returns:
            Self for method chaining
        """
        self.cancel_button.click()
        return self

    def has_validation_error(self) -> bool:
        """Check if the name input has a validation error

        Returns:
            True if the input has an error class, False otherwise
        """
        name_input_container = Element(By.LOCATOR, ".input.error")
        return name_input_container.is_visible()

    def get_error_message(self) -> str:
        """Get the error message text

        Returns:
            The error message text
        """
        return self.error_message.get_text()

    def is_create_button_enabled(self) -> bool:
        """Check if the Create button is enabled

        Returns:
            True if the button is enabled, False otherwise
        """
        return self.create_button.is_enabled()
