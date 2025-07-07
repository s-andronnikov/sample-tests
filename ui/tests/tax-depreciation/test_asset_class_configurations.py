import pytest

from config import base_settings
from ui.decorators.auth_decorator import UserRole, with_auth
from ui.pages.asset_class_page import AssetClassPage
from ui.pages.login_page import LoginPage


@pytest.fixture
def asset_class_page() -> AssetClassPage:
    """Return a AssetClassPage instance"""
    return AssetClassPage()


@pytest.mark.ui
class TestAssetClassConfigurations:

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
