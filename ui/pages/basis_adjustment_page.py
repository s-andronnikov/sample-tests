from faker import Faker

from framework.ui.element import By, Element, BaseElement
from ui.helpers.ag_grid_helper import AgGridHelper
from ui.helpers.url_helper import UrlHelper
from ui.pages.base_page import BasePage
from ui.pages.components.basis_adjustment_dialog import BasisAdjustmentDialog

fake = Faker()


class BasisAdjustmentPage(BasePage):
    """Basis Adjustment Configurations page object"""

    # The URL is set dynamically when opening the page
    url = None

    # Page elements
    title_element = Element(By.LOCATOR, "h3:has-text('Basis Adjustment')")
    grid_container = Element(By.LOCATOR, ".configuration-table")

    # Create basis adjustment elements
    create_button = Element(By.LOCATOR, "button:has-text('Create')")

    # Delete confirmation elements
    confirmation_popup = Element(By.LOCATOR, ".confirmation")
    confirmation_header = Element(By.LOCATOR, ".header", confirmation_popup)
    confirmation_delete_button = Element(By.LOCATOR, "button:has-text('Delete')", confirmation_popup)

    # Toaster message
    toaster_message = Element(By.LOCATOR, ".Toastify__toast-body")

    col_id_name = "name"
    col_id_actions = "actions"

    def __init__(self):
        super().__init__()
        self.ag_grid = AgGridHelper()
        self.basis_adjustment_dialog = BasisAdjustmentDialog()

    def open_with_id(self, depr_case_id: str):
        """Open the basis adjustment page with the given depreciation ID"""
        self.url = UrlHelper.depreciation_basis_adjustment(depr_case_id)
        return self.open()

    def is_page_loaded(self) -> bool:
        """Check if the page is loaded successfully"""
        self.title_element.should_be_visible()
        self.grid_container.should_be_visible()
        return True

    def verify_grid_headers(self, expected_headers):
        """Verify that the grid has the expected headers"""
        actual_headers = self.ag_grid.get_header_texts(self.grid_container)

        for header in expected_headers:
            assert header in actual_headers, f"Header '{header}' not found in grid headers: {actual_headers}"
        return self

    def click_create_button(self):
        """Click the Create button to open the basis adjustment creation form"""
        self.create_button.click()
        self.basis_adjustment_dialog.should_be_visible()
        return self

    def fill_basis_adjustment_form(self, name=None):
        """Fill the basis adjustment creation form

        Args:
            name: Name for the basis adjustment (random if not provided)

        Returns:
            The name used for the basis adjustment
        """
        return self.basis_adjustment_dialog.fill_form(name)

    def submit_form(self):
        """Submit the basis adjustment form"""
        self.basis_adjustment_dialog.create()

        # Wait for the form to disappear
        self.basis_adjustment_dialog.should_not_be_visible()
        return self

    def cancel_form(self):
        """Cancel the form without submitting"""
        self.basis_adjustment_dialog.cancel()
        self.basis_adjustment_dialog.should_not_be_visible()
        return self

    def verify_basis_adjustment_in_grid(self, name):
        """Verify that a basis adjustment with the given name appears in the grid

        Args:
            name: The name of the basis adjustment to look for

        Returns:
            True if the basis adjustment is found, False otherwise
        """
        # Wait for grid to fully load
        self.grid_container.should_be_visible()

        for row in self.ag_grid.get_grid_body_rows().all():
            if self.ag_grid.get_cell_by_row_and_text(name, row).is_visible():
                return True
        return False

    def select_first_row(self) -> BaseElement:
        """Select the first row in the grid"""
        self.grid_container.should_be_visible()
        return self.ag_grid.get_grid_body_row_position(1, self.grid_container)

    def get_name_value_by_row(self, row: BaseElement) -> str:
        """Get the name value from a row"""
        name_cell = self.ag_grid.get_grid_body_row_cell_by_col_id(row, self.col_id_name)
        return name_cell.get_text()

    def get_actions_cell(self, row):
        """Get the actions cell for a row"""
        return self.ag_grid.get_grid_body_row_cell_by_col_id(row, self.col_id_actions)

    def click_edit_icon(self, actions_cell: BaseElement):
        """Click the edit icon that appears when hovering over Actions cell

        Returns:
            Self for method chaining
        """
        edit_icon = Element(By.LOCATOR, ".pencil", parent=actions_cell)
        edit_icon.should_be_visible().click()

        # Verify dialog appears
        self.basis_adjustment_dialog.should_be_visible()
        return self

    def edit_basis_adjustment_name(self, new_name):
        """Edit the basis adjustment name in the edit form

        Args:
            new_name: The new name for the basis adjustment

        Returns:
            Self for method chaining
        """
        self.basis_adjustment_dialog.name_input.should_be_visible()
        current_name = self.basis_adjustment_dialog.name_input._get_locator().input_value()
        self.basis_adjustment_dialog.name_input.fill(new_name)
        return self, current_name

    def save_edited_form(self):
        """Save the edited form by clicking the Save button

        Returns:
            Self for method chaining
        """
        self.basis_adjustment_dialog.save()
        self.basis_adjustment_dialog.should_not_be_visible()
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

    def verify_delete_confirmation_popup(self, basis_adjustment_name: str):
        """Verify that the delete confirmation popup is displayed with the correct content

        Args:
            basis_adjustment_name: The name of the basis adjustment being deleted

        Returns:
            Self for method chaining
        """
        self.confirmation_popup.should_be_visible()
        header_text = self.confirmation_header.get_text()
        expected_text = f"Delete Basis Adjustment {basis_adjustment_name}"

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
