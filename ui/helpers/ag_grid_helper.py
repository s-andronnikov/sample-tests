from playwright.sync_api import Locator
from framework.ui.element import BaseElement, By, Element


class AgGridHelper:
    """Helper class for working with AG-Grid components"""

    @staticmethod
    def get_grid_container(parent: BaseElement | None = None) -> BaseElement:
        """Get the AG-Grid container element"""
        locator = ".ag-root-wrapper"
        return Element(By.LOCATOR, locator, parent=parent)

    @staticmethod
    def get_header_row(parent: BaseElement | None = None) -> BaseElement:
        """Get the header row of the AG-Grid"""
        container = AgGridHelper.get_grid_container(parent)
        return container.chain(Element(By.LOCATOR, ".ag-header-row"))

    @staticmethod
    def get_header_cells(parent: BaseElement | None = None) -> BaseElement:
        """Get all header cells of the AG-Grid"""
        header_row = AgGridHelper.get_header_row(parent)
        return header_row.chain(Element(By.LOCATOR, ".ag-header-cell"))

    @staticmethod
    def get_header_cell_by_text(text: str, parent: BaseElement | None = None) -> BaseElement:
        """Get a header cell by its text content"""
        header_row = AgGridHelper.get_header_row(parent)
        return header_row.chain(Element(By.LOCATOR, f'.ag-header-cell:has-text("{text}")'))

    @staticmethod
    def get_header_texts(parent: BaseElement | None = None) -> list[str]:
        """Get the text of all header cells"""
        locator = AgGridHelper.get_header_cells(parent)._get_locator()
        # Get all header cell elements and extract their text
        cells = locator.all()
        texts = []
        for cell in cells:
            # Look for the div with the text content (AG-Grid structure observed)
            text_div = cell.locator(".ag-header-cell-text")
            if text_div.count() > 0:
                texts.append(text_div.text_content().strip())
            else:
                # Fallback to the cell's text content
                texts.append(cell.text_content().strip())
        return [text for text in texts if text]  # Filter out empty strings

    @staticmethod
    def get_row(index: int, parent: BaseElement | None = None) -> BaseElement:
        """Get a specific row by index"""
        container = AgGridHelper.get_grid_container(parent)
        return container.chain(Element(By.LOCATOR, f"[role='row'][row-index='{index}']"))

    @staticmethod
    def get_cell(row_index: int, column_id: str, parent: BaseElement | None = None) -> BaseElement:
        """Get a specific cell by row index and column id"""
        row = AgGridHelper.get_row(row_index, parent)
        return row.chain(Element(By.LOCATOR, f'.ag-cell[col-id="{column_id}"]'))

    @staticmethod
    def get_rows(parent: BaseElement | None = None) -> list[Locator]:
        return Element(By.LOCATOR, "[role='row']", parent=parent).all()

    def get_rows_count(self, parent: BaseElement | None = None) -> int:
        return len(self.get_rows(parent))

    @staticmethod
    def get_cell_by_row_and_header(row, header_text: str, parent: BaseElement | None = None) -> BaseElement:
        """Get a cell by row and header text

        Args:
            row: The row element
            header_text: The text of the header to find the column for
            parent: Optional parent element

        Returns:
            The cell element
        """
        # Get all header texts
        header_texts = AgGridHelper.get_header_texts(parent)

        # Special case for common columns
        if header_text == "Name":
            # Name is typically the first column
            return Element(By.LOCATOR, "[role='gridcell']:first-child", parent=row)
        elif header_text == "Actions":
            # Actions is typically the last column
            return Element(By.LOCATOR, "[role='gridcell']:last-child", parent=row)

        # For other headers, try to find the index
        try:
            # Find the index of the header with the specified text
            if header_text in header_texts:
                column_index = header_texts.index(header_text)
                # Use 1-based indexing for CSS nth-child
                return Element(By.LOCATOR, f"[role='gridcell']:nth-child({column_index + 1})", parent=row)
        except Exception:
            # If we can't determine by index, fall back to content matching
            pass

        # Fall back to getting all cells and finding by content
        return Element(By.LOCATOR, "[role='gridcell']", parent=row)

    @staticmethod
    def get_cell_by_row_and_text(row, header_text: str) -> BaseElement:
        """Get a cell by row index and header text"""
        return Element(By.LOCATOR, f"[role='gridcell']:has-text(\"{header_text}\")", parent=row)
