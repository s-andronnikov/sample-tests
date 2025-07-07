from playwright.sync_api import Page

from framework.ui.driver import Driver


class BasePage:
    """Base class for all pages"""

    url: str = None

    def open(self):
        """Open the page"""
        Driver.goto(self.url)
        return self

    @staticmethod
    def get_page() -> Page:
        """Return the current page from the driver"""
        return Driver.get_driver()
