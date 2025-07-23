import pytest

from config import base_settings
from ui.pages.tax_depreciation.basis_adjustment_page import BasisAdjustmentPage


@pytest.mark.ui
class TestBasisAdjustmentConfigurations:
    page: BasisAdjustmentPage = None

    @pytest.fixture(autouse=True)
    def setup_authenticated_page(self, authenticated_basis_adjustment_page: BasisAdjustmentPage) -> BasisAdjustmentPage:
        """Setup authenticated page once for all tests in this class"""
        authenticated_basis_adjustment_page.open_with_id(base_settings.depr_case_id)
        assert authenticated_basis_adjustment_page.is_page_loaded(), "Basis adjustment configurations page failed to load"
        # Store the page instance on the class for all test methods to use
        self.page = authenticated_basis_adjustment_page

        return authenticated_basis_adjustment_page

    def test_basis_adjustment_configurations_page_loads(self):
        """Test that the basis adjustment configurations page loads successfully with correct grid headers"""
        # Constants
        expected_headers = ["Name", "Isolated", "Adjustment Type", "Excluded Sets of Books", "Tags", "Actions"]

        # Verify the grid headers
        self.page.verify_grid_headers(expected_headers)

    # @pytest.mark.skip()
    def test_create_basis_adjustment(self):
        """Test creating a new basis adjustment"""
        # Click the Create button to open the form
        self.page.click_create_button()
        # Verify form is visible
        self.page.basis_adjustment_dialog.should_be_visible()

        # Fill the form with random name, select adjustment type, excluded books, and tags
        basis_adjustment_name = self.page.fill_basis_adjustment_form()

        # Submit the form
        self.page.submit_form()

        # Verify the form is no longer visible (submitted successfully)
        self.page.basis_adjustment_dialog.should_not_be_visible()

        # Wait for grid to reload after creation
        self.page.wait_for_grid_reload()

        # Verify the new basis adjustment appears in the grid
        assert self.page.verify_basis_adjustment_in_grid(
            basis_adjustment_name
        ), f"Basis adjustment '{basis_adjustment_name}' not found in grid after creation"

    # @pytest.mark.skip()
    def test_edit_basis_adjustment(self):
        """Test editing a basis adjustment name"""
        first_row = self.page.select_first_row()
        first_row.click()

        original_name = self.page.get_name_value_by_row(first_row)

        # Get the Actions cell for the selected row
        actions_cell = self.page.get_actions_cell(first_row)

        # Click on edit icon
        self.page.click_edit_icon(actions_cell)

        # Verify edit form appears with the correct title
        self.page.basis_adjustment_dialog.should_be_visible()

        # Check that the form title contains the original name
        form_title_text = self.page.basis_adjustment_dialog.form_title.get_text()
        assert f"Edit {original_name}" in form_title_text, f"Expected form title to contain 'Edit {original_name}', got '{form_title_text}'"

        # Modify the name by adding 'Updated' prefix
        new_name = f"-Updated {original_name}"
        self.page.edit_basis_adjustment_name(new_name)

        # Save the changes
        self.page.save_edited_form()

        # Verify the edit form disappears
        self.page.basis_adjustment_dialog.should_not_be_visible()

        # Wait for grid reload
        self.page.wait_for_grid_reload()

        # Verify the grid contains a row with the updated name
        assert self.page.verify_basis_adjustment_in_grid(new_name), f"Basis adjustment '{new_name}' not found in grid after editing"

    # @pytest.mark.skip()
    def test_delete_basis_adjustment(self):
        """Test deleting a basis adjustment from the grid and verifying the operation is successful"""
        # Select the first row in the basis adjustment grid
        first_row = self.page.select_first_row()
        first_row.click()

        # Get the name of the selected basis adjustment
        basis_adjustment_name = self.page.get_name_value_by_row(first_row)

        # Get the Actions cell for the selected row
        actions_cell = self.page.get_actions_cell(first_row)

        # Click on the delete icon
        self.page.click_delete_icon(actions_cell)

        # Verify the delete confirmation popup appears with the correct content
        self.page.verify_delete_confirmation_popup(basis_adjustment_name)

        # Confirm deletion
        self.page.confirm_delete()

        # Verify deletion was successful
        self.page.verify_delete_success()

        # Wait for grid to reload after deletion
        self.page.wait_for_grid_reload()

        # Verify the deleted basis adjustment no longer appears in the grid
        assert not self.page.verify_basis_adjustment_in_grid(
            basis_adjustment_name
        ), f"Basis adjustment '{basis_adjustment_name}' still found in grid after deletion"

    # @pytest.mark.skip()
    def test_basis_adjustment_name_uniqueness_validation(self):
        """Test validation for unique basis adjustment names"""
        # Get an existing basis adjustment name from the grid

        if len(self.page.ag_grid.get_grid_body_rows().all()) == 0:
            # Create a new basis adjustment if grid is empty
            self.page.click_create_button()
            basis_adjustment_name = self.page.fill_basis_adjustment_form()
            self.page.submit_form()
            self.page.wait_for_grid_reload()
        else:
            # Get the name of the first basis adjustment in the grid
            first_row = self.page.select_first_row()
            basis_adjustment_name = self.page.get_name_value_by_row(first_row)

        # Try to create a new basis adjustment with the same name
        self.page.click_create_button()
        self.page.basis_adjustment_dialog.name_input.fill(basis_adjustment_name)

        # Fill the rest of the required fields
        self.page.basis_adjustment_dialog.adjustment_type_select.click()
        type_options = self.page.basis_adjustment_dialog.adjustment_type_options.all()
        if type_options:
            type_options[0].click()

        self.page.basis_adjustment_dialog.form_container.click()

        # Verify validation error is shown after filling in duplicate name
        assert self.page.basis_adjustment_dialog.has_validation_error(), "No validation error shown for duplicate name"

        # Verify error message
        error_message = self.page.basis_adjustment_dialog.get_error_message()
        assert "already exists" in error_message or "must be unique" in error_message, f"Unexpected error message: {error_message}"

        # Verify create button is disabled
        assert (
            not self.page.basis_adjustment_dialog.is_create_button_enabled()
        ), "Create button should be disabled when validation error exists"

        # Cancel the form
        self.page.cancel_form()
