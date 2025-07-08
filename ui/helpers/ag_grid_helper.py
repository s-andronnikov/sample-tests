from framework.ui.element import BaseElement, By, Element

ATTR_ROW_INDEX = "row-index"
ATTR_ROW_ID = "row-id"
ATTR_COL_ID = "col-id"


class AgGridHelper:
    """Helper class for working with AG-Grid components"""

    loc_grid_container = ".ag-root-wrapper"

    loc_grip_header_wrapper = ".ag-header"
    loc_grid_header_container = ".ag-header-container[role='rowgroup']"
    loc_grip_header_column = "[role='columnheader']"
    loc_grip_header_column_name = ".ag-header-cell-text"

    loc_grid_body_wrapper = ".ag-body"
    loc_grid_body_container = ".ag-center-cols-container[role='rowgroup']"
    loc_grid_body_row = "[role='row']"
    loc_grid_body_cell = "[role='gridcell']"

    def get_grid_container(self, parent: BaseElement | None = None) -> BaseElement:
        return Element(By.LOCATOR, self.loc_grid_container, parent=parent)

    def get_grid_header_container(self, parent: BaseElement | None = None) -> BaseElement:
        return Element(By.LOCATOR, self.loc_grid_header_container, parent=parent)

    def get_grid_header_columns(self, parent: BaseElement | None = None) -> BaseElement:
        return self.get_grid_header_container(parent).chain(Element(By.LOCATOR, self.loc_grip_header_column))

    def get_grid_header_column_names(self, parent: BaseElement) -> BaseElement:
        return self.get_grid_header_columns(parent).chain(Element(By.LOCATOR, self.loc_grip_header_column_name))

    def get_grid_header_column_by_col_id(self, col_id: str, parent: BaseElement | None = None) -> BaseElement:
        return self.get_grid_header_container(parent).chain(Element(By.LOCATOR, f"[{ATTR_COL_ID}='{col_id}']"))

    def get_grid_body_container(self, parent: BaseElement | None = None) -> BaseElement:
        return Element(By.LOCATOR, self.loc_grid_body_container, parent=parent)

    def get_grid_body_rows(self, parent: BaseElement | None = None) -> BaseElement:
        return self.get_grid_body_container(parent).chain(Element(By.LOCATOR, self.loc_grid_body_row))

    def get_grid_body_row_by_index(self, index: int, parent: BaseElement | None = None) -> BaseElement:
        return self.get_grid_body_container(parent).chain(Element(By.LOCATOR, f"[role='row'][row-index='{index}']"))

    def get_grid_body_row_by_row_id(self, row_id: str, parent: BaseElement | None = None) -> BaseElement:
        return self.get_grid_body_container(parent).chain(Element(By.LOCATOR, f"[{ATTR_ROW_ID}='{row_id}']"))

    def get_grid_body_row_position(self, position: int, parent: BaseElement | None = None) -> BaseElement:
        return self.get_grid_body_container(parent).chain(Element(By.LOCATOR, f"[role='row']:nth-child({position})"))

    def get_grid_body_row_cells(self, row: BaseElement, parent: BaseElement | None = None) -> BaseElement:
        return row.chain(Element(By.LOCATOR, self.loc_grid_body_cell))

    def get_grid_body_cells_by_col_id(self, col_id: str, parent: BaseElement | None = None) -> BaseElement:
        return self.get_grid_body_container(parent).chain(Element(By.LOCATOR, f"[{ATTR_COL_ID}='{col_id}']"))

    @staticmethod
    def get_grid_body_row_cell_by_col_id(row: BaseElement, col_id: str, parent: BaseElement | None = None) -> BaseElement:
        return row.chain(Element(By.LOCATOR, f"[{ATTR_COL_ID}='{col_id}']"))

    def get_header_texts(self, parent: BaseElement | None = None) -> list[str]:
        """Get the text of all header cells"""
        elements = self.get_grid_header_column_names(parent).all()
        return [el.text_content().strip() for el in elements]

    def get_cell_by_row_and_text(self, header_text: str, parent: BaseElement | None = None) -> BaseElement:
        """Get a cell by row index and header text"""
        return Element(By.LOCATOR, f'{self.loc_grid_body_cell}:has-text("{header_text}")', parent=parent)
