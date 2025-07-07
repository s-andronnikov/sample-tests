from faker import Faker

from framework.ui.element import By, Element
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
    grid_container = Element(By.LOCATOR, ".ag-root-wrapper")

    # Create asset class elements
    create_button = Element(By.LOCATOR, "button:has-text('Create')")
    form_wrapper = Element(By.LOCATOR, "[class='configurations-form-wrapper']")

    form_container = Element(By.LOCATOR, "form", form_wrapper)
    name_input = Element(By.LOCATOR, "input[name='name']")

    depreciation_profile_element = Element(By.LOCATOR, "[name='deprProfileId'][role='combobox']", form_container)
    depreciation_profile_select = Element(By.LOCATOR, "i", parent=depreciation_profile_element)
    depreciation_profile_options = Element(By.LOCATOR, "[role='option']", parent=depreciation_profile_element)

    form_tags_element = Element(By.LOCATOR, ".dimensional-tag", form_container)
    form_tags_select = Element(By.LOCATOR, "i", parent=form_tags_element)
    form_tags_options = Element(By.LOCATOR, "[class='result']", parent=form_tags_element)

    action_buttons_wrapper = Element(By.LOCATOR, "[class='action-buttons']", form_wrapper)
    action_button_cancel = Element(By.LOCATOR, "button:has-text('Cancel')", action_buttons_wrapper)
    action_button_create = Element(By.LOCATOR, "button:has-text('Create')", action_buttons_wrapper)

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

    @staticmethod
    def get_grid_headers():
        """Get the text of all grid headers"""
        return AgGridHelper.get_header_texts()

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
        # self.form_tags_select.click()
        #
        # # Get all tag options and select the first two if available
        # tag_options = self.form_tags_options.all()
        # if tag_options:
        #     tag_options[0].click()

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

        for row in self.ag_grid.get_rows():
            if self.ag_grid.get_cell_by_row_and_text(row, name).is_visible():
                return True
        return False
