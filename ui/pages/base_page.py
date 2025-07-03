from framework.ui.driver import Driver


class BasePage:
    """Base class for all pages"""

    url: str = None

    def open(self):
        """Open the page"""
        Driver.goto(self.url)
        return self
