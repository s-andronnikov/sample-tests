from faker import Faker

from framework.ui.element import By, Element, BaseElement
from ui.helpers.ag_grid_helper import AgGridHelper
from ui.helpers.url_helper import UrlHelper
from ui.pages.base_page import BasePage

fake = Faker()


class AssetClassPage(BasePage):
    """Asset Class Configurations page object"""

    # The URL is set dynamically when opening the page
    url = None

    # Page elements
    title_element = Element(By.LOCATOR, "h3:has-text('Asset Class')")
    grid_container = Element(By.LOCATOR, ".configuration-table")

    # Create asset class elements
    create_button = Element(By.LOCATOR, "button:has-text('Create')")
    form_wrapper = Element(By.LOCATOR, "[class='configurations-form-wrapper']")

    form_container = Element(By.LOCATOR, "form", form_wrapper)
    name_input = Element(By.LOCATOR, "input[name='name']")
    form_title = Element(By.LOCATOR, "p.title", form_wrapper)

    depreciation_profile_element = Element(By.LOCATOR, "[name='deprProfileId'][role='combobox']", form_container)
    depreciation_profile_select = Element(By.LOCATOR, "i", parent=depreciation_profile_element)
    depreciation_profile_options = Element(By.LOCATOR, "[role='option']", parent=depreciation_profile_element)

    form_tags_element = Element(By.LOCATOR, ".field.dimensional-tag", form_container)
    form_tags_select = Element(By.LOCATOR, "input", parent=form_tags_element)
    form_tags_options = Element(By.LOCATOR, "[class='result']", parent=form_tags_element)

    action_buttons_wrapper = Element(By.LOCATOR, "[class='action-buttons']", form_wrapper)
    action_button_cancel = Element(By.LOCATOR, "button:has-text('Cancel')", action_buttons_wrapper)
    action_button_create = Element(By.LOCATOR, "button:has-text('Create')", action_buttons_wrapper)
    action_button_save = Element(By.LOCATOR, "button:has-text('Save')", action_buttons_wrapper)

    col_id_name = "name"
    col_id_actions = "actions"

    def __init__(self):
        super().__init__()
        self.ag_grid = AgGridHelper()

    def open_with_id(self, depreciation_id: str):
        """Open the asset class page with the given depreciation ID"""
        self.url = UrlHelper.depreciation_asset_class(depreciation_id)
        return self.open()

    def is_page_loaded(self) -> bool:
        """Check if the page is loaded successfully"""
        self.title_element.should_be_visible()
        self.grid_container.should_be_visible()
        return True

    def get_grid_headers(self):
        """Get the text of all grid headers"""
        return self.ag_grid.get_header_texts(self.grid_container)

    def verify_grid_headers(self, expected_headers):
        """Verify that the grid has the expected headers"""
        actual_headers = self.get_grid_headers()

        for header in expected_headers:
            assert header in actual_headers, f"Header '{header}' not found in grid headers: {actual_headers}"
        return self

    def click_create_button(self):
        """Click the Create button to open the asset class creation form"""
        self.create_button.click()
        self.form_container.should_be_visible()
        return self

    def fill_asset_class_form(self, name=None):
        """Fill the asset class creation form

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
        # First click on the dropdown to open it
        self.depreciation_profile_select.click()

        # Wait for options to be visible and select the first non-empty option
        profile_options = self.depreciation_profile_options().all()
        if profile_options:
            profile_options[0].click()

        # # Select the first and second tags
        self.form_tags_select.click()

        # Get all tag options and select the first two if available
        tag_options = self.form_tags_options.all()
        if tag_options:
            tag_options[0].click()

        return name

    def submit_form(self):
        """Submit the asset class form"""
        self.action_button_create.should_be_enabled().click()

        # Wait for the form to disappear or for the grid to refresh
        self.form_container.should_be_visible(should_visible=False)
        return self

    def verify_asset_class_in_grid(self, name):
        """Verify that an asset class with the given name appears in the grid

        Args:
            name: The name of the asset class to look for

        Returns:
            True if the asset class is found, False otherwise
        """
        # Wait for grid to fully load
        self.grid_container.should_be_visible()

        for row in self.ag_grid.get_grid_body_rows().all():
            if self.ag_grid.get_cell_by_row_and_text(name, row).is_visible():
                return True
        return False

    def select_first_row(self) -> BaseElement:
        self.grid_container.should_be_visible()

        return self.ag_grid.get_grid_body_row_position(1, self.grid_container)

    def get_name_value_by_row(self, row: BaseElement) -> str:
        name_cell = self.ag_grid.get_grid_body_row_cell_by_col_id(row, self.col_id_name)

        return name_cell.get_text()

    def get_actions_cell(self, row):
        return self.ag_grid.get_grid_body_row_cell_by_col_id(row, self.col_id_actions)

    def click_edit_icon(self, actions_cell: BaseElement):
        """Click the edit icon that appears when hovering over Actions cell

        Returns:
            Self for method chaining
        """
        edit_icon = Element(By.LOCATOR, ".pencil", parent=actions_cell)
        edit_icon.should_be_visible().click()

        return self

    def edit_asset_class_name(self, new_name):
        """Edit the asset class name in the edit form

        Args:
            new_name: The new name for the asset class

        Returns:
            Self for method chaining
        """
        self.name_input.should_be_visible()
        current_name = self.name_input._get_locator().input_value()
        self.name_input.fill(new_name)
        return self, current_name

    def save_edited_form(self):
        """Save the edited form by clicking the Save button

        Returns:
            Self for method chaining
        """
        self.action_button_save.should_be_enabled().click()
        self.form_container.should_be_visible(should_visible=False)
        return self
