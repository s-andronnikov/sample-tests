from collections.abc import Callable
from typing import Generic, Optional, TypeVar

from playwright.sync_api import Locator

from framework.ui.element import BaseElement, By

T = TypeVar("T")


class ListElement(BaseElement, Generic[T]):
    """Base class for list elements with iteration support"""

    def __init__(
        self,
        search_by: str,
        locator: str,
        item_factory: Callable[[Locator, int], T],
        parent: BaseElement | Locator | None = None,
        ignore_parent: bool = False,
    ):
        super().__init__(search_by, locator, parent, ignore_parent)
        self.item_factory = item_factory

    def __iter__(self):
        locator = self._get_locator()
        count = locator.count()
        for i in range(count):
            yield self.item_factory(locator.nth(i), i)

    def __getitem__(self, index: int) -> T:
        return self.item_factory(self._get_locator().nth(index), index)

    def count(self) -> int:
        return self._get_locator().count()

    def filter(self, predicate: Callable[[T], bool]) -> list[T]:
        return [item for item in self if predicate(item)]

    def find(self, predicate: Callable[[T], bool]) -> T | None:
        for item in self:
            if predicate(item):
                return item
        return None


class Grid(BaseElement):
    """Grid component with row and cell access"""

    def __init__(
        self,
        search_by: str = By.LOCATOR,
        locator: str = "table",
        parent: BaseElement | Locator | None = None,
    ):
        super().__init__(search_by, locator, parent)
        self.rows = ListElement(By.LOCATOR, "tbody > tr", lambda loc, idx: GridRow(loc, idx, self), self)

    def get_row(self, index: int) -> "GridRow":
        return self.rows[index]

    def find_row_by_text(self, text: str) -> Optional["GridRow"]:
        return self.rows.find(lambda row: text in row.get_text())


class GridRow:
    """Grid row with cell access"""

    def __init__(self, locator: Locator, index: int, grid: Grid):
        self.locator = locator
        self.index = index
        self.grid = grid
        self.cells = ListElement(By.LOCATOR, "td", lambda loc, idx: GridCell(loc, idx, self), locator)

    def get_cell(self, index: int) -> "GridCell":
        return self.cells[index]

    def get_text(self) -> str:
        return self.locator.text_content() or ""

    def click(self):
        self.locator.click()
        return self


class GridCell:
    """Grid cell"""

    def __init__(self, locator: Locator, index: int, row: GridRow):
        self.locator = locator
        self.index = index
        self.row = row

    def get_text(self) -> str:
        return self.locator.text_content() or ""

    def click(self):
        self.locator.click()
        return self
