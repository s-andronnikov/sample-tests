import pytest

from config import base_settings
from ui.pages.basis_adjustment_page import BasisAdjustmentPage


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

    def test_create_basis_adjustment(self):
        """Test creating a new basis adjustment"""
        # Click the Create button to open the form
        self.page.click_create_button()
        # Verify form is visible
        assert self.page.form_container.is_visible(), "Create form did not appear"

        # Fill the form with random name, select adjustment type, excluded books, and tags
        basis_adjustment_name = self.page.fill_basis_adjustment_form()
        print(f"Created basis adjustment with name: {basis_adjustment_name}")

        # Submit the form
        self.page.submit_form()

        # Verify the form is no longer visible (submitted successfully)
        assert not self.page.form_container.is_visible(), "Form is still visible after submission"

        # Wait for grid to reload after creation
        self.page.wait_for_grid_reload()

        # Verify the new basis adjustment appears in the grid
        assert self.page.verify_basis_adjustment_in_grid(
            basis_adjustment_name
        ), f"Basis adjustment '{basis_adjustment_name}' not found in grid after creation"

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
        self.page.form_container.should_be_visible()

        # Check that the form title contains the original name
        form_title_text = self.page.form_title.get_text()
        assert f"Edit {original_name}" in form_title_text, f"Expected form title to contain 'Edit {original_name}', got '{form_title_text}'"

        # Modify the name by adding 'Updated' prefix
        new_name = f"Updated {original_name}"
        self.page.edit_basis_adjustment_name(new_name)

        # Save the changes
        self.page.save_edited_form()

        # Verify the edit form disappears
        assert not self.page.form_container.is_visible(), "Edit form is still visible after submission"

        # Wait for grid reload
        self.page.wait_for_grid_reload()

        # Verify the grid contains a row with the updated name
        assert self.page.verify_basis_adjustment_in_grid(new_name), f"Basis adjustment '{new_name}' not found in grid after editing"

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

    def test_form_validation_and_cancellation(self):
        """Test form validation and cancellation operations"""
        # Test form validation
        self.page.click_create_button()
        # Try to submit without filling required fields
        self.page.action_button_create.click()

        # Form should still be visible (validation failed)
        assert self.page.form_container.is_visible(), "Form should remain visible when validation fails"

        # Test form cancellation
        self.page.cancel_form()
        assert not self.page.form_container.is_visible(), "Form should be hidden after cancellation"

        # Test edit cancellation
        if self.page.ag_grid.get_grid_body_rows().count() > 0:
            first_row = self.page.select_first_row()
            first_row.click()

            actions_cell = self.page.get_actions_cell(first_row)
            self.page.click_edit_icon(actions_cell)

            # Make a change then cancel
            self.page.name_input.fill("Cancelled Edit Operation")
            self.page.cancel_form()

            # Form should be hidden after cancellation
            assert not self.page.form_container.is_visible(), "Edit form should be hidden after cancellation"
