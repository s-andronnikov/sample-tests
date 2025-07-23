import pytest

from config import base_settings
from ui.pages.depreciation_profile_page import DepreciationProfilePage


@pytest.mark.ui
class TestDepreciationProfileConfigurations:
    page: DepreciationProfilePage = None

    @pytest.fixture(autouse=True)
    def setup_authenticated_page(self, authenticated_depreciation_profile_page: DepreciationProfilePage) -> DepreciationProfilePage:
        """Setup authenticated page once for all tests in this class"""
        authenticated_depreciation_profile_page.open_with_id(base_settings.depr_case_id)
        assert authenticated_depreciation_profile_page.is_page_loaded(), "Depreciation profile configurations page failed to load"
        # Store the page instance on the class for all test methods to use
        self.page = authenticated_depreciation_profile_page

        return authenticated_depreciation_profile_page

    def test_depreciation_profile_configurations_page_loads(self):
        """Test that the depreciation profile configurations page loads successfully with correct grid headers"""
        # Constants
        expected_headers = [
            "Name",
            "Profile Description",
            "Class Life",
            "Bonus Eligible",
            "Mid-Quarter Eligible",
            "Amortization",
            "Rate Type",
            "Method",
            "Convention",
            "Life",
            "Tags",
            "Actions",
        ]

        # Verify the page title
        assert "Depreciation Profiles" in self.page.get_page_title(), "Page title does not contain 'Depreciation Profiles'"

        # Verify the grid headers
        self.page.verify_grid_headers(expected_headers)

    def test_create_depreciation_profile(self):
        """Test creating a new depreciation profile"""
        # Click the Create button to open the form
        self.page.click_create_button()
        # Verify form is visible
        self.page.depreciation_profile_dialog.should_be_visible()

        # Fill the form with random name
        profile_name = self.page.fill_depreciation_profile_form()

        # Submit the form
        self.page.submit_form()

        # Verify the form is no longer visible (submitted successfully)
        self.page.depreciation_profile_dialog.should_not_be_visible()

        # Wait for grid to reload after creation
        self.page.wait_for_grid_reload()

        # Verify the new depreciation profile appears in the grid
        assert self.page.verify_depreciation_profile_in_grid(
            profile_name
        ), f"Depreciation profile '{profile_name}' not found in grid after creation"

    def test_edit_depreciation_profile(self):
        """Test editing a depreciation profile name"""
        # Select the first row in the grid
        first_row = self.page.select_first_row()
        first_row.click()

        # Get the original name of the selected profile
        original_name = self.page.get_name_value_by_row(first_row)

        # Get the Actions cell for the selected row
        actions_cell = self.page.get_actions_cell(first_row)

        # Click on edit icon
        self.page.click_edit_icon(actions_cell)

        # Verify edit form appears with the correct title
        self.page.depreciation_profile_dialog.should_be_visible()

        # Check that the form title contains the original name
        form_title_text = self.page.depreciation_profile_dialog.form_title.get_text()
        assert f"Edit {original_name}" in form_title_text, f"Expected form title to contain 'Edit {original_name}', got '{form_title_text}'"

        # Modify the name by adding 'Updated' prefix
        new_name = f"Updated {original_name}"
        self.page.edit_depreciation_profile_name(new_name)

        # Save the changes
        self.page.save_edited_form()

        # Verify the edit form disappears
        self.page.depreciation_profile_dialog.should_not_be_visible()

        # Wait for grid reload
        self.page.wait_for_grid_reload()

        # Verify the grid contains a row with the updated name
        assert self.page.verify_depreciation_profile_in_grid(new_name), f"Depreciation profile '{new_name}' not found in grid after editing"

    def test_delete_depreciation_profile(self):
        """Test deleting a depreciation profile from the grid"""
        # Select the first row in the grid
        first_row = self.page.select_first_row()
        first_row.click()

        # Get the name of the selected profile
        profile_name = self.page.get_name_value_by_row(first_row)

        # Get the Actions cell for the selected row
        actions_cell = self.page.get_actions_cell(first_row)

        # Click on the delete icon
        self.page.click_delete_icon(actions_cell)

        # Verify the delete confirmation popup appears with the correct content
        self.page.verify_delete_confirmation_popup(profile_name)

        # Confirm deletion
        self.page.confirm_delete()

        # Verify deletion was successful
        self.page.verify_delete_success()

        # Wait for grid to reload after deletion
        self.page.wait_for_grid_reload()

        # Verify the deleted profile no longer appears in the grid
        assert not self.page.verify_depreciation_profile_in_grid(
            profile_name
        ), f"Depreciation profile '{profile_name}' still found in grid after deletion"

    def test_depreciation_profile_name_uniqueness_validation(self):
        """Test validation for unique depreciation profile names"""
        # Get an existing profile name from the grid
        if len(self.page.ag_grid.get_grid_body_rows(self.page.grid_container).all()) == 0:
            # Create a new profile if grid is empty
            self.page.click_create_button()
            profile_name = self.page.fill_depreciation_profile_form()
            self.page.submit_form()
            self.page.wait_for_grid_reload()
        else:
            # Get the name of the first profile in the grid
            first_row = self.page.select_first_row()
            profile_name = self.page.get_name_value_by_row(first_row)

        # Try to create a new profile with the same name
        self.page.click_create_button()
        self.page.depreciation_profile_dialog.name_input.fill(profile_name)

        # Click somewhere else on the form to trigger validation
        self.page.depreciation_profile_dialog.form_container.click()

        # Verify validation error is shown after filling in duplicate name
        assert self.page.depreciation_profile_dialog.has_validation_error(), "No validation error shown for duplicate name"

        # Verify error message
        error_message = self.page.depreciation_profile_dialog.get_error_message()
        assert "already exists" in error_message or "must be unique" in error_message, f"Unexpected error message: {error_message}"

        # Verify create button is disabled
        assert (
            not self.page.depreciation_profile_dialog.is_create_button_enabled()
        ), "Create button should be disabled when validation error exists"

        # Cancel the form
        self.page.cancel_form()
