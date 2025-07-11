from faker import Faker

from framework.ui.element import BaseElement, By

fake = Faker()


class AssetClassDialog:
    """Asset class dialog component for adding/editing asset classes"""

    def __init__(self, parent: BaseElement | None = None):
        self.parent = parent

        # Dialog elements
        self.form_wrapper = BaseElement(By.LOCATOR, "[class='configurations-form-wrapper']", parent)
        self.form_container = BaseElement(By.LOCATOR, "form", self.form_wrapper)
        self.form_title = BaseElement(By.LOCATOR, "p.title", self.form_wrapper)

        # Form inputs
        self.name_input = BaseElement(By.LOCATOR, "input[name='name']", self.form_container)

        # Depreciation profile selection
        self.depreciation_profile_element = BaseElement(By.LOCATOR, "[name='deprProfileId'][role='combobox']", self.form_container)
        self.depreciation_profile_select = BaseElement(By.LOCATOR, "i", self.depreciation_profile_element)
        self.depreciation_profile_options = BaseElement(By.LOCATOR, "[role='option']", self.depreciation_profile_element)

        # Tags selection
        self.tags_element = BaseElement(By.LOCATOR, ".field.dimensional-tag", self.form_container)
        self.tags_select = BaseElement(By.LOCATOR, "input", self.tags_element)
        self.tags_options = BaseElement(By.LOCATOR, "[class='result']", self.tags_element)

        # Buttons
        self.action_buttons_wrapper = BaseElement(By.LOCATOR, "[class='action-buttons']", self.form_wrapper)
        self.create_button = BaseElement(By.LOCATOR, "button:has-text('Create')", self.action_buttons_wrapper)
        self.save_button = BaseElement(By.LOCATOR, "button:has-text('Save')", self.action_buttons_wrapper)
        self.cancel_button = BaseElement(By.LOCATOR, "button:has-text('Cancel')", self.action_buttons_wrapper)

        # Validation elements
        self.name_input_container = BaseElement(By.LOCATOR, "div.input:has(input[name='name'])", self.form_container)
        self.error_message = BaseElement(By.LOCATOR, ".labeled-error", self.form_container)

    def fill_form(self, name=None):
        """Fill the asset class form

        Args:
            name: Name for the asset class (random if not provided)

        Returns:
            The name used for the asset class
        """
        # Generate a random name if not provided
        if name is None:
            name = f"111 Test Asset Class {fake.word()} {fake.random_int(100, 999)}"

        # Fill the name field
        self.name_input.fill(name)

        # Select the first depreciation profile
        self.depreciation_profile_select.click()

        # Wait for options to be visible and select the first non-empty option
        profile_options = self.depreciation_profile_options.all()
        if profile_options:
            profile_options[0].click()

        # Select the first tag
        self.tags_select.click()

        # Get all tag options and select the first one if available
        tag_options = self.tags_options.all()
        if tag_options:
            tag_options[0].click()

        return name

    def create(self):
        """Click the create button to submit the form"""
        self.create_button.should_be_enabled().click()
        return self

    def save(self):
        """Click the save button to submit an edit form"""
        self.save_button.should_be_enabled().click()
        return self

    def cancel(self):
        """Click the cancel button"""
        self.cancel_button.click()
        return self

    def should_be_visible(self):
        """Check if the dialog is visible"""
        self.form_container.should_be_visible()
        return self

    def should_not_be_visible(self):
        """Check if the dialog is not visible"""
        self.form_container.should_be_visible(should_visible=False)
        return self

    def has_validation_error(self):
        """Check if the form has validation errors"""
        return "error" in self.name_input_container.get_class_list()

    def get_error_message(self):
        """Get the error message text"""
        return self.error_message.get_text()

    def is_create_button_enabled(self):
        """Check if the create button is enabled"""
        return self.create_button.is_enabled()
