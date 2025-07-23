from framework.ui.element import Element, By, BaseElement
from random import randint


class DepreciationProfileDialog:
    """Dialog component for creating and editing depreciation profiles"""

    def __init__(self, parent: BaseElement | None = None):
        self.parent = parent

        self.form_container = Element(By.LOCATOR, ".configurations-form-wrapper")
        self.form_title = Element(By.LOCATOR, ".title", self.form_container)
        self.name_input = Element(By.LOCATOR, "input[name='name']", self.form_container)
        self.description_input = Element(By.LOCATOR, "textarea[name='description']", self.form_container)

        # Dropdown fields
        self.class_life_dropdown = Element(By.LOCATOR, "[name='classLife']", self.form_container)
        self.rate_type_dropdown = Element(By.LOCATOR, "[name='rateType']", self.form_container)
        self.method_dropdown = Element(By.LOCATOR, "[name='method']", self.form_container)
        self.convention_dropdown = Element(By.LOCATOR, "[name='convention']", self.form_container)

        # Checkbox fields
        self.bonus_eligible_checkbox = Element(By.LOCATOR, "input[name='bonusEligible']", self.form_container)
        self.mid_quarter_eligible_checkbox = Element(By.LOCATOR, "input[name='midQuarterEligible']", self.form_container)
        self.amortization_checkbox = Element(By.LOCATOR, "input[name='amortization']", self.form_container)

        # Life input
        self.life_input = Element(By.LOCATOR, "input[name='life']", self.form_container)

        # Tags selector
        self.tags_dropdown = Element(By.LOCATOR, "[name='tags']", self.form_container)

        # Dropdown options container (general for all dropdowns)
        self.dropdown_options_container = Element(By.LOCATOR, "[role='listbox']")
        self.dropdown_options = Element(By.LOCATOR, "[role='option']", self.dropdown_options_container)

        # Action buttons
        self.action_buttons_wrapper = Element(By.LOCATOR, ".action-buttons", self.form_container)
        self.create_button = Element(By.LOCATOR, "button:has-text('Create')", self.action_buttons_wrapper)
        self.save_button = Element(By.LOCATOR, "button:has-text('Save')", self.action_buttons_wrapper)
        self.cancel_button = Element(By.LOCATOR, "button:has-text('Cancel')", self.action_buttons_wrapper)
        self.error_message = Element(By.LOCATOR, ".labeled-error", self.form_container)

    def fill_form(self, name: str | None = None) -> str:
        """Fill the depreciation profile creation form with minimal required fields

        Args:
            name: Name for the depreciation profile (random if not provided)

        Returns:
            The name used for the depreciation profile
        """
        # Generate random name if not provided
        if name is None:
            name = f"Test Depreciation Profile {randint(1000, 9999)}"

        # Fill name field
        self.name_input.fill(name)

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

    def should_be_visible(self):
        """Check if the dialog is visible"""
        self.form_container.should_be_visible()
        return self

    def should_not_be_visible(self):
        """Check if the dialog is not visible"""
        self.form_container.should_be_visible(should_visible=False)
        return self
