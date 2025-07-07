from framework.ui.element import By, Element
from ui.helpers.ag_grid_helper import AgGridHelper
from ui.helpers.url_helper import UrlHelper
from ui.pages.base_page import BasePage


class AssetClassPage(BasePage):
    """Asset Class Configurations page object"""

    # The URL is set dynamically when opening the page
    url = None

    # Page elements
    title_element = Element(By.LOCATOR, "h3:has-text('Asset Class')")
    grid_container = Element(By.LOCATOR, ".ag-root-wrapper")

    def __init__(self):
        super().__init__()
        self.ag_grid = AgGridHelper()

    def open_with_id(self, depreciation_id: str):
        """Open the asset class page with the given depreciation ID"""
        self.url = UrlHelper.depreciation_asset_class(depreciation_id)
        return self.open()

    def is_page_loaded(self) -> bool:
        """Check if the page is loaded successfully"""
        self.title_element.should_be_visible()
        self.grid_container.should_be_visible()
        return True

    def get_grid_headers(self):
        """Get the text of all grid headers"""
        return AgGridHelper.get_header_texts()

    def verify_grid_headers(self, expected_headers):
        """Verify that the grid has the expected headers"""
        actual_headers = self.get_grid_headers()
        for header in expected_headers:
            assert header in actual_headers, f"Header '{header}' not found in grid headers: {actual_headers}"
        return self
