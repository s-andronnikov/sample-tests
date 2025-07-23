import pytest

from config import base_settings
from ui.pages.tax_depreciation.asset_class_page import AssetClassPage


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
        """Test that the tax_depreciation asset class configurations page loads successfully with correct grid headers"""
        # Constants
        expected_headers = ["Name", "Depreciation Profile", "Tags", "Actions"]

        # Verify the grid headers
        self.page.verify_grid_headers(expected_headers)

    # @pytest.mark.skip()
    def test_create_asset_class(self):
        """Test creating a new asset class"""
        # Click the Create button to open the form
        self.page.click_create_button()
        # Verify form is visible
        assert self.page.asset_class_dialog.should_be_visible(), "Create form did not appear"

        # Fill the form with random name, select first depreciation profile, and first two tags
        asset_class_name = self.page.fill_asset_class_form()
        print(f"Created asset class with name: {asset_class_name}")

        # Submit the form
        self.page.submit_form()

        # Verify the form is no longer visible (submitted successfully)
        self.page.asset_class_dialog.should_not_be_visible()

        # Wait for grid to reload after deletion
        self.page.wait_for_grid_reload()

        # Verify the new asset class appears in the grid
        assert self.page.verify_asset_class_in_grid(asset_class_name), f"Asset class '{asset_class_name}' not found in grid after creation"

    # @pytest.mark.skip()
    def test_asset_class_name_uniqueness_validation(self):
        """Test that the asset class creation form validates uniqueness of names"""
        # Get name from first record on the list grid
        first_row = self.page.select_first_row()
        existing_name = self.page.get_name_value_by_row(first_row)

        # Click the Create button to open the form
        self.page.click_create_button()
        assert self.page.asset_class_dialog.should_be_visible(), "Create form did not appear"

        # Fill the Name input on form with existing record name
        self.page.asset_class_dialog.name_input.fill(existing_name)

        # Click on form to trigger change event
        self.page.asset_class_dialog.form_container.click()

        # Verify validation error appears
        # 1. div.input should have class - error
        assert self.page.asset_class_dialog.has_validation_error(), "Name input does not have error class"

        # 2. ".labeled-error" should appear with text "Name must be unique."
        error_message_text = self.page.asset_class_dialog.get_error_message()
        assert "Name must be unique." in error_message_text, f"Expected error message 'Name must be unique.' but got '{error_message_text}'"

        # 3. Button "Create" should become disabled
        assert not self.page.asset_class_dialog.is_create_button_enabled(), "Create button should be disabled when validation error exists"

        # Clean up - cancel the form
        self.page.cancel_form()

    # @pytest.mark.skip()
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
        self.page.asset_class_dialog.should_be_visible()

        # Check that the form title contains the original name
        form_title_text = self.page.asset_class_dialog.form_title.get_text()
        assert f"Edit {original_name}" in form_title_text, f"Expected form title to contain 'Edit {original_name}', got '{form_title_text}'"

        # Modify the name by adding '112' prefix
        new_name = f"112 {original_name}"
        self.page.edit_asset_class_name(new_name)

        # Verify the Save button becomes active and click it
        self.page.save_edited_form()

        # Verify the edit form disappears
        self.page.asset_class_dialog.should_not_be_visible()

        # Verify the grid contains a row with the updated name
        assert self.page.verify_asset_class_in_grid(new_name), f"Asset class '{new_name}' not found in grid after editing"

    # @pytest.mark.skip()
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
