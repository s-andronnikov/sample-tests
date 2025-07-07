import pytest
from playwright.async_api import expect

from framework.ui.driver import Driver
from ui.pages.asset_class_page import AssetClassPage


@pytest.mark.ui
class TestAssetClass:
    @pytest.mark.asyncio
    async def test_asset_class_page_loads(self):
        """Test that the asset class configuration page loads successfully"""
        # Arrange
        asset_class_page = AssetClassPage()

        # Act
        await asset_class_page.open()

        # Assert
        await asset_class_page.verify_page_loaded()

    @pytest.mark.asyncio
    async def test_asset_class_grid_headers(self):
        """Test that the asset class grid has the expected headers"""
        # Arrange
        asset_class_page = AssetClassPage()

        # Act
        await asset_class_page.open()

        # Assert
        await asset_class_page.verify_grid_headers()
import pytest
from playwright.sync_api import expect

from framework.ui.driver import Driver
from ui.pages.asset_class_page import AssetClassPage


@pytest.mark.ui
class TestAssetClass:
    def test_asset_class_page_loads(self):
        """Test that the asset class configuration page loads successfully"""
        # Arrange
        asset_class_page = AssetClassPage()

        # Act
        asset_class_page.open()

        # Assert
        asset_class_page.verify_page_loaded()

    def test_asset_class_grid_headers(self):
        """Test that the asset class grid has the expected headers"""
        # Arrange
        asset_class_page = AssetClassPage()

        # Act
        asset_class_page.open()

        # Assert
        asset_class_page.verify_grid_headers()

    def test_asset_class_grid_has_data(self):
        """Test that the asset class grid loads with data"""
        # Arrange
        asset_class_page = AssetClassPage()

        # Act
        asset_class_page.open()

        # Assert
        asset_class_page.verify_grid_has_data()

    def test_asset_class_page_navigation(self):
        """Test direct navigation to the asset class configuration page"""
        # Arrange
        page = Driver.get_driver()
        url = "http://localhost:3000/depreciation/9aa52b3f-f76d-438d-9557-92984bd9e1fc/configurations/asset-class"

        # Act
        Driver.goto(url)
        page.wait_for_load_state("networkidle")

        # Assert
        expect(page).to_have_url(url)
        expect(page.locator("h3:has-text('Asset Class')")).to_be_visible()

        # Verify grid headers
        grid_headers = page.locator("[role='columnheader']")
        expect(grid_headers.nth(0)).to_contain_text("Name")
        expect(grid_headers.nth(1)).to_contain_text("Depreciation Profile")
        expect(grid_headers.nth(2)).to_contain_text("Tags")
        expect(grid_headers.nth(3)).to_contain_text("Actions")

        # Verify grid has data
        rows = page.locator("[role='rowgroup']:nth-child(2) > [role='row']")
        assert rows.count() > 0, "Expected grid to have at least one row of data"
    @pytest.mark.asyncio
    async def test_asset_class_grid_has_data(self):
        """Test that the asset class grid loads with data"""
        # Arrange
        asset_class_page = AssetClassPage()

        # Act
        await asset_class_page.open()

        # Assert
        await asset_class_page.verify_grid_has_data()

    @pytest.mark.asyncio
    async def test_asset_class_page_navigation(self):
        """Test direct navigation to the asset class configuration page"""
        # Arrange
        page = Driver.get_driver()
        url = "http://localhost:3000/depreciation/9aa52b3f-f76d-438d-9557-92984bd9e1fc/configurations/asset-class"

        # Act
        await Driver.goto(url)
        await page.wait_for_load_state("networkidle")

        # Assert
        await expect(page).to_have_url(url)
        await expect(page.locator("h3:has-text('Asset Class')")).to_be_visible()

        # Verify grid headers
        grid_headers = page.locator("[role='columnheader']")
        await expect(grid_headers.nth(0)).to_contain_text("Name")
        await expect(grid_headers.nth(1)).to_contain_text("Depreciation Profile")
        await expect(grid_headers.nth(2)).to_contain_text("Tags")
        await expect(grid_headers.nth(3)).to_contain_text("Actions")

        # Verify grid has data
        rows = page.locator("[role='rowgroup']:nth-child(2) > [role='row']")
        assert await rows.count() > 0, "Expected grid to have at least one row of data"
