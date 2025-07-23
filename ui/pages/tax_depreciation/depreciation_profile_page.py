from framework.ui.element import Element, By
from ui.pages.base_page import BasePage
from ui.helpers.ag_grid_helper import AgGridHelper
from ui.helpers.url_helper import UrlHelper
from ui.pages.tax_depreciation.components.depreciation_profile_dialog import DepreciationProfileDialog


class DepreciationProfilePage(BasePage):
    """Depreciation Profile Configurations page object"""

    # The URL is set dynamically when opening the page
    url = None

    # Page elements
    title_element = Element(By.LOCATOR, "h3:has-text('Depreciation Profile')")
    grid_container = Element(By.LOCATOR, ".configuration-table")

    # Create depreciation profile elements
    create_button = Element(By.LOCATOR, "button:has-text('Create')")

    # Delete confirmation elements
    confirmation_popup = Element(By.LOCATOR, ".confirmation")
    confirmation_header = Element(By.LOCATOR, ".header", confirmation_popup)
    confirmation_delete_button = Element(By.LOCATOR, "button:has-text('Delete')", confirmation_popup)

    # Toaster message
    toaster_message = Element(By.LOCATOR, ".Toastify__toast-body")

    # Column IDs for accessing grid cells
    col_id_name = "name"
    col_id_description = "description"
    col_id_class_life = "classLife"
    col_id_bonus_eligible = "bonusEligible"
    col_id_mid_quarter_eligible = "midQuarterEligible"
    col_id_amortization = "amortization"
    col_id_rate_type = "rateType"
    col_id_method = "method"
    col_id_convention = "convention"
    col_id_life = "life"
    col_id_tags = "tags"
    col_id_actions = "actions"

    def __init__(self):
        super().__init__()
        self.ag_grid = AgGridHelper()
        self.depreciation_profile_dialog = DepreciationProfileDialog()

    def open_with_id(self, depr_case_id: str):
        """Open the depreciation profile page with the given depreciation ID"""
        self.url = UrlHelper.depreciation_profile(depr_case_id)
        return self.open()

    def get_page_title(self) -> str:
        """Get the page title

        Returns:
            The page title text
        """
        return self.browser_driver.title

    def is_page_loaded(self) -> bool:
        """Check if the page is loaded successfully"""
        self.title_element.should_be_visible()
        self.grid_container.should_be_visible()
        self.wait_for_grid_reload()
        return True

    def verify_grid_headers(self, expected_headers: list[str]):
        """Verify that the grid has the expected headers

        Args:
            expected_headers: List of expected header texts

        Returns:
            Self for method chaining
        """
        actual_headers = self.ag_grid.get_header_texts(self.grid_container)

        for header in expected_headers:
            assert header in actual_headers, f"Header '{header}' not found in grid headers: {actual_headers}"
        return self

    def wait_for_grid_reload(self):
        """Wait for the grid to reload after an operation such as deletion

        Returns:
            Self for method chaining
        """
        # First ensure the grid container is visible
        self.grid_container.should_be_visible()

        # Wait for the grid to stabilize after data reload
        # This uses the grid's internal loading indicator or checks for row presence
        self.ag_grid.wait_for_grid_loading_to_finish(self.grid_container)

        return self

    def select_first_row(self):
        """Select the first row in the grid

        Returns:
            The selected row element
        """
        # Get all grid rows
        rows = self.ag_grid.get_grid_body_rows(self.grid_container).all()
        # Make sure we have at least one row
        assert len(rows) > 0, "No rows found in the grid"
        # Return the first row
        return rows[0]

    def get_name_value_by_row(self, row):
        """Get the name value from the row

        Args:
            row: The row element to get the name from

        Returns:
            The name text
        """
        name_cell = self.ag_grid.get_cell_by_col_id(row, self.col_id_name)
        return name_cell.get_text()

    def get_actions_cell(self, row):
        """Get the actions cell for the row

        Args:
            row: The row element to get the actions cell from

        Returns:
            The actions cell element
        """
        return self.ag_grid.get_cell_by_col_id(row, self.col_id_actions)

    def click_edit_icon(self, actions_cell):
        """Click the edit icon in the actions cell

        Args:
            actions_cell: The actions cell containing the edit icon

        Returns:
            Self for method chaining
        """
        # Hover over the actions cell to show the action buttons
        actions_cell.hover()
        # Find and click the edit icon (pencil icon)
        edit_icon = Element(By.LOCATOR, ".edit", actions_cell)
        edit_icon.should_be_visible()
        edit_icon.click()
        return self

    def click_delete_icon(self, actions_cell):
        """Click the delete icon in the actions cell

        Args:
            actions_cell: The actions cell containing the delete icon

        Returns:
            Self for method chaining
        """
        # Hover over the actions cell to show the action buttons
        actions_cell.hover()
        # Find and click the delete icon (trash icon)
        delete_icon = Element(By.LOCATOR, ".trash", actions_cell)
        delete_icon.should_be_visible()
        delete_icon.click()
        return self

    def verify_delete_confirmation_popup(self, profile_name: str):
        """Verify that the delete confirmation popup appears with the correct content

        Args:
            profile_name: The name of the profile being deleted

        Returns:
            Self for method chaining
        """
        self.confirmation_popup.should_be_visible()
        header_text = self.confirmation_header.get_text()
        assert (
            f"Delete Depreciation Profile {profile_name}" in header_text
        ), f"Expected header to contain 'Delete Depreciation Profile {profile_name}', got '{header_text}'"
        self.confirmation_delete_button.should_be_visible()
        assert self.confirmation_delete_button.is_enabled(), "Delete button should be enabled"
        return self

    def confirm_delete(self):
        """Confirm deletion by clicking the Delete button in the confirmation popup

        Returns:
            Self for method chaining
        """
        self.confirmation_delete_button.click()
        return self

    def verify_delete_success(self):
        """Verify that the deletion was successful

        Returns:
            Self for method chaining
        """
        # Confirmation popup should be gone
        self.confirmation_popup.should_be_visible(should_visible=False)
        # Success message should appear
        self.toaster_message.should_be_visible()
        message_text = self.toaster_message.get_text()
        assert "Successfully Deleted" in message_text, f"Expected success message to contain 'Successfully Deleted', got '{message_text}'"
        return self

    def click_create_button(self):
        """Click the Create button to open the form

        Returns:
            Self for method chaining
        """
        self.create_button.click()
        return self

    def fill_depreciation_profile_form(self, name: str | None = None) -> str:
        """Fill the depreciation profile creation form

        Args:
            name: Optional name for the profile (random if not provided)

        Returns:
            The name used for the profile
        """
        return self.depreciation_profile_dialog.fill_form(name)

    def submit_form(self):
        """Submit the form by clicking the Create button

        Returns:
            Self for method chaining
        """
        self.depreciation_profile_dialog.create()
        return self

    def cancel_form(self):
        """Cancel the form by clicking the Cancel button

        Returns:
            Self for method chaining
        """
        self.depreciation_profile_dialog.cancel()
        return self

    def edit_depreciation_profile_name(self, new_name: str):
        """Edit the depreciation profile name

        Args:
            new_name: The new name to set

        Returns:
            Self for method chaining
        """
        self.depreciation_profile_dialog.name_input.fill(new_name)
        return self

    def save_edited_form(self):
        """Save the edited form by clicking the Save button

        Returns:
            Self for method chaining
        """
        self.depreciation_profile_dialog.save()
        return self

    def verify_depreciation_profile_in_grid(self, profile_name: str) -> bool:
        """Verify that a depreciation profile with the given name exists in the grid

        Args:
            profile_name: The name of the profile to look for

        Returns:
            True if the profile is found, False otherwise
        """
        # Get all grid rows
        rows = self.ag_grid.get_grid_body_rows(self.grid_container).all()
        # Check if any row has the profile name
        for row in rows:
            name_cell = self.ag_grid.get_cell_by_col_id(row, self.col_id_name)
            if profile_name in name_cell.get_text():
                return True
        return False
