from typing import List, Optional

from playwright.async_api import Locator

from framework.ui.driver import Driver
from framework.ui.element import Element, By


class AGGrid:
    """Helper class for working with AG-Grid components"""

    def __init__(self, grid_locator: str):
        self.grid_locator = grid_locator
        self.grid = Element(By.LOCATOR, grid_locator)
        self.headers = Element(By.LOCATOR, f"{grid_locator} [role='columnheader']")
        self.rows = Element(By.LOCATOR, f"{grid_locator} [role='rowgroup']:nth-child(2) > [role='row']")
from typing import List

from framework.ui.driver import Driver
from framework.ui.element import Element, By


class AGGrid:
    """Helper class for working with AG-Grid components"""

    def __init__(self, grid_locator: str):
        self.grid_locator = grid_locator
        self.grid = Element(By.LOCATOR, grid_locator)
        self.headers = Element(By.LOCATOR, f"{grid_locator} [role='columnheader']")
        self.rows = Element(By.LOCATOR, f"{grid_locator} [role='rowgroup']:nth-child(2) > [role='row']")

    def get_header_names(self) -> List[str]:
        """Get the list of header names"""
        page = Driver.get_driver()
        headers = page.locator(f"{self.grid_locator} [role='columnheader']")
        count = headers.count()

        header_names = []
        for i in range(count):
            header = headers.nth(i)
            name = header.text_content()
            if name:
                header_names.append(name.strip())

        return header_names

    def get_row_count(self) -> int:
        """Get the number of rows in the grid"""
        page = Driver.get_driver()
        rows = page.locator(f"{self.grid_locator} [role='rowgroup']:nth-child(2) > [role='row']")
        return rows.count()

    def get_cell_value(self, row_index: int, col_index: int) -> str:
        """Get the text content of a cell at the specified row and column index"""
        page = Driver.get_driver()
        row = page.locator(f"{self.grid_locator} [role='rowgroup']:nth-child(2) > [role='row']:nth-child({row_index + 1})")
        cell = row.locator(f"[role='gridcell']:nth-child({col_index + 1})")
        return cell.text_content() or ""

    def click_cell(self, row_index: int, col_index: int):
        """Click on a cell at the specified row and column index"""
        page = Driver.get_driver()
        row = page.locator(f"{self.grid_locator} [role='rowgroup']:nth-child(2) > [role='row']:nth-child({row_index + 1})")
        cell = row.locator(f"[role='gridcell']:nth-child({col_index + 1})")
        cell.click()
    async def get_header_names(self) -> List[str]:
        """Get the list of header names"""
        page = Driver.get_driver()
        headers = page.locator(f"{self.grid_locator} [role='columnheader']")
        count = await headers.count()

        header_names = []
        for i in range(count):
            header = headers.nth(i)
            name = await header.text_content()
            if name:
                header_names.append(name.strip())

        return header_names

    async def get_row_count(self) -> int:
        """Get the number of rows in the grid"""
        page = Driver.get_driver()
        rows = page.locator(f"{self.grid_locator} [role='rowgroup']:nth-child(2) > [role='row']")
        return await rows.count()

    async def get_cell_value(self, row_index: int, col_index: int) -> str:
        """Get the text content of a cell at the specified row and column index"""
        page = Driver.get_driver()
        row = page.locator(f"{self.grid_locator} [role='rowgroup']:nth-child(2) > [role='row']:nth-child({row_index + 1})")
        cell = row.locator(f"[role='gridcell']:nth-child({col_index + 1})")
        return await cell.text_content() or ""

    async def click_cell(self, row_index: int, col_index: int):
        """Click on a cell at the specified row and column index"""
        page = Driver.get_driver()
        row = page.locator(f"{self.grid_locator} [role='rowgroup']:nth-child(2) > [role='row']:nth-child({row_index + 1})")
        cell = row.locator(f"[role='gridcell']:nth-child({col_index + 1})")
        await cell.click()
