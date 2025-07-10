import pytest

from config import base_settings
from ui.pages.asset_class_page import AssetClassPage


@pytest.mark.ui
class TestAssetClassConfigurations:
    page: AssetClassPage = None

    @pytest.fixture(autouse=True)
    def setup_authenticated_page(self, authenticated_asset_class_page: AssetClassPage) -> AssetClassPage:
        """Setup authenticated page once for all tests in this class"""
        authenticated_asset_class_page.open_with_id(base_settings.depr_case_id)
        assert authenticated_asset_class_page.is_page_loaded(), "Asset class configurations page failed to load"
        # Store the page instance on the class for all test methods to use
        self.page = authenticated_asset_class_page

        return authenticated_asset_class_page

    def test_asset_class_configurations_page_loads(self):
        """Test that the tax-depreciation asset class configurations page loads successfully with correct grid headers"""
        # Constants
        expected_headers = ["Name", "Depreciation Profile", "Tags", "Actions"]

        # Verify the grid headers
        self.page.verify_grid_headers(expected_headers)

    def test_create_asset_class(self):
        """Test creating a new asset class"""
        # Click the Create button to open the form
        self.page.click_create_button()
        # Verify form is visible
        assert self.page.form_container.is_visible(), "Create form did not appear"

        # Fill the form with random name, select first depreciation profile, and first two tags
        asset_class_name = self.page.fill_asset_class_form()
        print(f"Created asset class with name: {asset_class_name}")

        # Submit the form
        self.page.submit_form()

        # Verify the form is no longer visible (submitted successfully)
        assert not self.page.form_container.is_visible(), "Form is still visible after submission"

        # Wait for grid to reload after deletion
        self.page.wait_for_grid_reload()

        # Verify the new asset class appears in the grid
        assert self.page.verify_asset_class_in_grid(asset_class_name), f"Asset class '{asset_class_name}' not found in grid after creation"

    def test_edit_asset_class_name(self):
        """Test editing an asset class name"""
        first_row = self.page.select_first_row()
        first_row.click()

        original_name = self.page.get_name_value_by_row(first_row)

        # Hover over the Actions cell for the selected row
        actions_cell = self.page.get_actions_cell(first_row)

        # Click on edit icon
        self.page.click_edit_icon(actions_cell)

        # Verify edit form appears with the correct title
        self.page.form_container.should_be_visible()

        # Check that the form title contains the original name
        form_title_text = self.page.form_title.get_text()
        assert f"Edit {original_name}" in form_title_text, f"Expected form title to contain 'Edit {original_name}', got '{form_title_text}'"

        # Modify the name by adding '112' prefix
        new_name = f"112 {original_name}"
        self.page.edit_asset_class_name(new_name)

        # Verify the Save button becomes active and click it
        self.page.save_edited_form()

        # Verify the edit form disappears
        assert not self.page.form_container.is_visible(), "Edit form is still visible after submission"

        # Verify the grid contains a row with the updated name
        assert self.page.verify_asset_class_in_grid(new_name), f"Asset class '{new_name}' not found in grid after editing"

    def test_delete_asset_class(self):
        """Test deleting an asset class from the grid and verifying the operation is successful"""
        # Select the first row in the asset class grid
        first_row = self.page.select_first_row()
        first_row.click()

        # Get the name of the selected asset class
        asset_class_name = self.page.get_name_value_by_row(first_row)

        # Get the Actions cell for the selected row
        actions_cell = self.page.get_actions_cell(first_row)

        # Click on the delete icon
        self.page.click_delete_icon(actions_cell)

        # Verify the delete confirmation popup appears with the correct content
        self.page.verify_delete_confirmation_popup(asset_class_name)

        # Confirm deletion
        self.page.confirm_delete()

        # Verify deletion was successful
        self.page.verify_delete_success()

        # Wait for grid to reload after deletion
        self.page.wait_for_grid_reload()

        # Verify the deleted asset class no longer appears in the grid
        assert not self.page.verify_asset_class_in_grid(
            asset_class_name
        ), f"Asset class '{asset_class_name}' still found in grid after deletion"
