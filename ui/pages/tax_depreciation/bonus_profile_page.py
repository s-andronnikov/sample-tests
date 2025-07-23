from framework.ui.element import Element, By, BaseElement
from ui.pages.base_page import BasePage
from ui.helpers.ag_grid_helper import AgGridHelper
from ui.helpers.url_helper import UrlHelper
from ui.pages.tax_depreciation.components.bonus_profile_dialog import BonusProfileDialog


class BonusProfilePage(BasePage):
    """Bonus Profile Configurations page object"""

    # The URL is set dynamically when opening the page
    url = None

    # Page elements
    title_element = Element(By.LOCATOR, "h3:has-text('Bonus Profile')")
    grid_container = Element(By.LOCATOR, ".configuration-table")

    # Create bonus profile elements
    create_button = Element(By.LOCATOR, "button:has-text('Create')")

    # Delete confirmation elements
    confirmation_popup = Element(By.LOCATOR, ".confirmation")
    confirmation_header = Element(By.LOCATOR, ".header", confirmation_popup)
    confirmation_delete_button = Element(By.LOCATOR, "button:has-text('Delete')", confirmation_popup)

    # Toaster message
    toaster_message = Element(By.LOCATOR, ".Toastify__toast-body")

    # Column IDs for accessing grid cells
    col_id_name = "name"
    col_id_bonus_calculation_method = "bonusCalculationMethod"
    col_id_bonus_percent = "bonusPercent"
    col_id_actions = "actions"

    def __init__(self):
        super().__init__()
        self.ag_grid = AgGridHelper()
        self.bonus_profile_dialog = BonusProfileDialog()

    def open_with_id(self, depr_case_id: str):
        """Open the bonus profile page with the given depreciation ID"""
        self.url = UrlHelper.depreciation_bonus_profile(depr_case_id)
        return self.open()

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

    def click_create_button(self):
        """Click the Create button to open the bonus profile creation form"""
        self.create_button.click()
        self.bonus_profile_dialog.should_be_visible()
        return self

    def fill_bonus_profile_form(self, name=None, bonus_calculation_method="Standard", bonus_percent=None):
        """Fill the bonus profile creation form

        Args:
            name: Name for the bonus profile (random if not provided)
            bonus_calculation_method: Method for bonus calculation (Standard by default)
            bonus_percent: Bonus percent value (random if not provided)

        Returns:
            The name used for the bonus profile
        """
        return self.bonus_profile_dialog.fill_form(name, bonus_calculation_method, bonus_percent)

    def submit_form(self):
        """Submit the bonus profile form"""
        self.bonus_profile_dialog.create()

        # Wait for the form to disappear
        self.bonus_profile_dialog.should_not_be_visible()
        return self

    def verify_bonus_profile_in_grid(self, name: str) -> bool:
        """Verify that a bonus profile with the given name appears in the grid

        Args:
            name: The name of the bonus profile to look for

        Returns:
            True if the bonus profile is found, False otherwise
        """
        # Wait for grid to fully load
        self.grid_container.should_be_visible()

        for row in self.ag_grid.get_grid_body_rows().all():
            if self.ag_grid.get_cell_by_row_and_text(name, row).is_visible():
                return True
        return False

    def select_first_row(self) -> BaseElement:
        """Select the first row in the grid

        Returns:
            The selected row element
        """
        self.grid_container.should_be_visible()
        return self.ag_grid.get_grid_body_row_position(1, self.grid_container)

    def get_name_value_by_row(self, row: BaseElement) -> str:
        """Get the name value from a row

        Args:
            row: The row element

        Returns:
            The name value
        """
        name_cell = self.ag_grid.get_grid_body_row_cell_by_col_id(row, self.col_id_name)
        return name_cell.get_text()

    def get_bonus_calculation_method_by_row(self, row: BaseElement) -> str:
        """Get the bonus calculation method value from a row

        Args:
            row: The row element

        Returns:
            The bonus calculation method value
        """
        method_cell = self.ag_grid.get_grid_body_row_cell_by_col_id(row, self.col_id_bonus_calculation_method)
        return method_cell.get_text()

    def get_bonus_percent_by_row(self, row: BaseElement) -> str:
        """Get the bonus percent value from a row

        Args:
            row: The row element

        Returns:
            The bonus percent value
        """
        percent_cell = self.ag_grid.get_grid_body_row_cell_by_col_id(row, self.col_id_bonus_percent)
        return percent_cell.get_text()

    def get_actions_cell(self, row: BaseElement) -> BaseElement:
        """Get the actions cell for a row

        Args:
            row: The row element

        Returns:
            The actions cell element
        """
        return self.ag_grid.get_grid_body_row_cell_by_col_id(row, self.col_id_actions)

    def click_edit_icon(self, actions_cell: BaseElement):
        """Click the edit icon that appears when hovering over Actions cell

        Args:
            actions_cell: The Actions cell containing the edit icon

        Returns:
            Self for method chaining
        """
        edit_icon = Element(By.LOCATOR, ".pencil", parent=actions_cell)
        edit_icon.should_be_visible().click()

        # Verify dialog appears
        self.bonus_profile_dialog.should_be_visible()

        return self

    def edit_bonus_profile_name(self, new_name: str):
        """Edit the bonus profile name in the edit form

        Args:
            new_name: The new name for the bonus profile

        Returns:
            Tuple of (self, current_name) for method chaining
        """
        self.bonus_profile_dialog.name_input.should_be_visible()
        current_name = self.bonus_profile_dialog.name_input._get_locator().input_value()
        self.bonus_profile_dialog.name_input.fill(new_name)
        return self, current_name

    def edit_bonus_percent(self, new_percent: float):
        """Edit the bonus percent in the edit form

        Args:
            new_percent: The new percent value

        Returns:
            Tuple of (self, current_percent) for method chaining
        """
        self.bonus_profile_dialog.bonus_percent_input.should_be_visible()
        current_percent = self.bonus_profile_dialog.bonus_percent_input._get_locator().input_value()
        self.bonus_profile_dialog.bonus_percent_input.fill(str(new_percent))
        return self, current_percent

    def save_edited_form(self):
        """Save the edited form by clicking the Save button

        Returns:
            Self for method chaining
        """
        self.bonus_profile_dialog.save()
        self.bonus_profile_dialog.should_not_be_visible()
        return self

    def click_delete_icon(self, actions_cell: BaseElement):
        """Click the delete icon that appears in the Actions cell

        Args:
            actions_cell: The Actions cell containing the delete icon

        Returns:
            Self for method chaining
        """
        delete_icon = Element(By.LOCATOR, ".trash", parent=actions_cell)
        delete_icon.should_be_visible().click()

        return self

    def verify_delete_confirmation_popup(self, bonus_profile_name: str):
        """Verify that the delete confirmation popup is displayed with the correct content

        Args:
            bonus_profile_name: The name of the bonus profile being deleted

        Returns:
            Self for method chaining
        """
        self.confirmation_popup.should_be_visible()
        header_text = self.confirmation_header.get_text()
        expected_text = f"Delete Bonus Profile {bonus_profile_name}"

        assert expected_text in header_text, f"Expected confirmation header to contain '{expected_text}', got '{header_text}'"
        self.confirmation_delete_button.should_be_enabled()

        return self

    def confirm_delete(self):
        """Confirm deletion by clicking the Delete button in the confirmation popup

        Returns:
            Self for method chaining
        """
        self.confirmation_delete_button.click()
        self.confirmation_popup.should_be_visible(should_visible=False)

        return self

    def verify_delete_success(self):
        """Verify that the deletion was successful by checking the toaster message

        Returns:
            Self for method chaining
        """
        self.toaster_message.should_be_visible()
        message_text = self.toaster_message.get_text()

        assert "Successfully Deleted" in message_text, f"Expected toaster message to contain 'Successfully Deleted', got '{message_text}'"

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

    def cancel_form(self):
        """Cancel the bonus profile form by clicking the Cancel button

        Returns:
            Self for method chaining
        """
        self.bonus_profile_dialog.cancel()
        self.bonus_profile_dialog.should_not_be_visible()
        return self
