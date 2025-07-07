from typing import List, Optional

from playwright.sync_api import Locator
from framework.ui.element import BaseElement, By, Element


class AgGridHelper:
    """Helper class for working with AG-Grid components"""

    @staticmethod
    def get_grid_container(parent: Optional[BaseElement] = None) -> BaseElement:
        """Get the AG-Grid container element"""
        locator = ".ag-root-wrapper"
        return Element(By.LOCATOR, locator, parent=parent)

    @staticmethod
    def get_header_row(parent: Optional[BaseElement] = None) -> BaseElement:
        """Get the header row of the AG-Grid"""
        container = AgGridHelper.get_grid_container(parent)
        return container.chain(Element(By.LOCATOR, ".ag-header-row"))

    @staticmethod
    def get_header_cells(parent: Optional[BaseElement] = None) -> BaseElement:
        """Get all header cells of the AG-Grid"""
        header_row = AgGridHelper.get_header_row(parent)
        return header_row.chain(Element(By.LOCATOR, ".ag-header-cell"))

    @staticmethod
    def get_header_cell_by_text(text: str, parent: Optional[BaseElement] = None) -> BaseElement:
        """Get a header cell by its text content"""
        header_row = AgGridHelper.get_header_row(parent)
        return header_row.chain(Element(By.LOCATOR, f".ag-header-cell:has-text(\"{text}\")"))

    @staticmethod
    def get_header_texts(parent: Optional[BaseElement] = None) -> List[str]:
        """Get the text of all header cells"""
        locator = AgGridHelper.get_header_cells(parent)._get_locator()
        # Get all header cell elements and extract their text
        cells = locator.all()
        texts = []
        for cell in cells:
            # Look for the div with the text content (AG-Grid structure observed)
            text_div = cell.locator('.ag-header-cell-text')
            if text_div.count() > 0:
                texts.append(text_div.text_content().strip())
            else:
                # Fallback to the cell's text content
                texts.append(cell.text_content().strip())
        return [text for text in texts if text]  # Filter out empty strings

    @staticmethod
    def get_row(index: int, parent: Optional[BaseElement] = None) -> BaseElement:
        """Get a specific row by index"""
        container = AgGridHelper.get_grid_container(parent)
        return container.chain(Element(By.LOCATOR, f".ag-row[row-index=\"{index}\"]"))

    @staticmethod
    def get_cell(row_index: int, column_id: str, parent: Optional[BaseElement] = None) -> BaseElement:
        """Get a specific cell by row index and column id"""
        row = AgGridHelper.get_row(row_index, parent)
        return row.chain(Element(By.LOCATOR, f".ag-cell[col-id=\"{column_id}\"]"))

    @staticmethod
    def get_rows_count(parent: Optional[BaseElement] = None) -> int:
        """Get the number of rows in the grid"""
        container = AgGridHelper.get_grid_container(parent)
        locator = container.chain(Element(By.LOCATOR, ".ag-row"))._get_locator()
        return locator.count()

    @staticmethod
    def get_cell_by_row_and_header(row_index: int, header_text: str, parent: Optional[BaseElement] = None) -> BaseElement:
        """Get a cell by row index and header text"""
        # This is a more complex operation as we need to find the column index from header text
        row = AgGridHelper.get_row(row_index, parent)
        return row.chain(Element(By.LOCATOR, f".ag-cell:has-text(\"{header_text}\")"))
