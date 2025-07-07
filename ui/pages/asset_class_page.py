from common.decorators import ui_url
from common.routes import UIRoutes
from framework.ui.element import By, Element
from ui.pages.base_page import BasePage
from common.decorators import ui_url
from common.routes import UIRoutes
from framework.ui.element import By, Element
from ui.pages.base_page import BasePage


@ui_url(UIRoutes.ASSET_CLASS)
class AssetClassPage(BasePage):
    """Asset Class configuration page model"""

    # Page elements
    title = Element(By.LOCATOR, "h3:has-text('Asset Class')")
    create_button = Element(By.LOCATOR, "button:has-text('Create')")

    # Grid elements
    grid = Element(By.LOCATOR, "[role='grid']")
    header_name = Element(By.LOCATOR, "[role='columnheader']:has-text('Name')")
    header_depreciation_profile = Element(By.LOCATOR, "[role='columnheader']:has-text('Depreciation Profile')")
    header_tags = Element(By.LOCATOR, "[role='columnheader']:has-text('Tags')")
    header_actions = Element(By.LOCATOR, "[role='columnheader']:has-text('Actions')")

    # AG-Grid specific elements
    grid_rows = Element(By.LOCATOR, "[role='rowgroup']:nth-child(2) > [role='row']")
    grid_cell = Element(By.LOCATOR, "[role='gridcell']")

    def verify_page_loaded(self):
        """Verify the asset class page is loaded correctly"""
        self.title.should_be_visible()
        self.grid.should_be_visible()
        return self

    def verify_grid_headers(self):
        """Verify that all required grid headers are present"""
        self.header_name.should_be_visible()
        self.header_depreciation_profile.should_be_visible()
        self.header_tags.should_be_visible()
        self.header_actions.should_be_visible()
        return self

    def verify_grid_has_data(self):
        """Verify that the grid has at least one row of data"""
        page = self.get_page()
        rows_count = page.locator("[role='rowgroup']:nth-child(2) > [role='row']").count()
        assert rows_count > 0, "Expected grid to have at least one row of data"
        return self

@ui_url(UIRoutes.ASSET_CLASS)
class AssetClassPage(BasePage):
    """Asset Class configuration page model"""

    # Page elements
    title = Element(By.LOCATOR, "h3:has-text('Asset Class')")
    create_button = Element(By.LOCATOR, "button:has-text('Create')")

    # Grid elements
    grid = Element(By.LOCATOR, "[role='grid']")
    header_name = Element(By.LOCATOR, "[role='columnheader']:has-text('Name')")
    header_depreciation_profile = Element(By.LOCATOR, "[role='columnheader']:has-text('Depreciation Profile')")
    header_tags = Element(By.LOCATOR, "[role='columnheader']:has-text('Tags')")
    header_actions = Element(By.LOCATOR, "[role='columnheader']:has-text('Actions')")

    # AG-Grid specific elements
    grid_rows = Element(By.LOCATOR, "[role='rowgroup']:nth-child(2) > [role='row']")
    grid_cell = Element(By.LOCATOR, "[role='gridcell']")

    async def verify_page_loaded(self):
        """Verify the asset class page is loaded correctly"""
        await self.title.should_be_visible()
        await self.grid.should_be_visible()
        return self

    async def verify_grid_headers(self):
        """Verify that all required grid headers are present"""
        await self.header_name.should_be_visible()
        await self.header_depreciation_profile.should_be_visible()
        await self.header_tags.should_be_visible()
        await self.header_actions.should_be_visible()
        return self

    async def verify_grid_has_data(self):
        """Verify that the grid has at least one row of data"""
        page = self.get_page()
        rows_count = await page.locator("[role='rowgroup']:nth-child(2) > [role='row']").count()
        assert rows_count > 0, "Expected grid to have at least one row of data"
        return self
