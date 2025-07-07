import pytest

from config import base_settings
from ui.pages.asset_class_page import AssetClassPage


@pytest.fixture
def asset_class_page() -> AssetClassPage:
    """Return a AssetClassPage instance"""
    return AssetClassPage()


@pytest.mark.ui
class TestAssetClassConfigurations:

    @pytest.mark.skip
    def test_asset_class_configurations_page_loads(self, authenticated_asset_class_page: AssetClassPage):
        """Test that the tax-depreciation asset class configurations page loads successfully with correct grid headers"""
        # Constants
        expected_headers = ["Name", "Depreciation Profile", "Tags", "Actions"]

        # Open the page with the specific depreciation ID from config
        authenticated_asset_class_page.open_with_id(base_settings.depreciation_id)

        # Verify the page loads successfully
        assert authenticated_asset_class_page.is_page_loaded(), "Asset class configurations page failed to load"

        # Verify the grid headers
        authenticated_asset_class_page.verify_grid_headers(expected_headers)

    def test_create_asset_class(self, authenticated_asset_class_page: AssetClassPage):
        """Test creating a new asset class"""
        # Open the asset class page with the specified depreciation ID
        authenticated_asset_class_page.open_with_id(base_settings.depreciation_id)

        # Verify the page loads successfully
        assert authenticated_asset_class_page.is_page_loaded(), "Asset class configurations page failed to load"

        # Click the Create button to open the form
        authenticated_asset_class_page.click_create_button()
        # Verify form is visible
        assert authenticated_asset_class_page.form_container.is_visible(), "Create form did not appear"

        # Fill the form with random name, select first depreciation profile, and first two tags
        asset_class_name = authenticated_asset_class_page.fill_asset_class_form()
        print(f"Created asset class with name: {asset_class_name}")

        # Submit the form
        authenticated_asset_class_page.submit_form()

        # Verify the form is no longer visible (submitted successfully)
        assert not authenticated_asset_class_page.form_container.is_visible(), "Form is still visible after submission"

        # Verify the new asset class appears in the grid
        assert authenticated_asset_class_page.verify_asset_class_in_grid(
            asset_class_name
        ), f"Asset class '{asset_class_name}' not found in grid after creation"
