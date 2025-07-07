from dataclasses import dataclass
from typing import Union

from playwright.sync_api import Locator, expect

from framework.ui.driver import Driver

OP_COMMON_TIMEOUT = 10000


@dataclass
class By:
    LOCATOR = "locator"
    TEXT = "get_by_text"
    LABEL = "get_by_label"
    TITLE = "get_by_title"
    ALT_TEXT = "get_by_alt_text"
    PLACEHOLDER = "get_by_placeholder"
    TEST_ID = "get_by_test_id"


class BaseElement:
    def __init__(
        self,
        search_by: str,
        locator: str,
        parent: Union["BaseElement", Locator] | None = None,
        ignore_parent: bool = False,
        exact_text: bool = True,
    ):
        self.search_by = search_by
        self.search_locator = locator
        self.parent = parent
        self.ignore_parent = ignore_parent
        self.exact_text = exact_text

    def __call__(self, *args, **kwargs):
        if kwargs.get("parent"):
            self.parent = kwargs["parent"]
        self._locator_kwargs = kwargs
        return self

    def _get_locator(self) -> Locator:
        locator: Locator
        if hasattr(self, "_locator_kwargs"):
            formatted_locator = self.search_locator.format(**self._locator_kwargs)
        elif hasattr(self, "search_locator"):
            formatted_locator = self.search_locator
        else:
            formatted_locator = ""

        driver = (
            (self.parent._get_locator() if isinstance(self.parent, BaseElement) else self.parent)
            if (self.parent and not self.ignore_parent)
            else Driver().get_driver()
        )
        resolve_method = getattr(driver, self.search_by)
        locator = resolve_method(formatted_locator)
        return locator

    def chain(self, element: "BaseElement"):
        element.parent = self
        return element

    def hover(self, **kwargs):
        self._get_locator().hover(**kwargs)
        return self

    def all(self) -> list[Locator]:
        return self._get_locator().all()

    def should_be_visible(self, should_visible: bool = True, timeout: int = OP_COMMON_TIMEOUT) -> "BaseElement":
        locator = self._get_locator()
        expect(locator).to_be_visible(visible=should_visible, timeout=timeout)
        return self

    def is_visible(self) -> bool:
        return self._get_locator().is_visible()

    def click(self, timeout: int = OP_COMMON_TIMEOUT, force: bool = False) -> "BaseElement":
        self._get_locator().click(timeout=timeout, force=force)
        return self

    def fill(self, value: str, timeout: int = OP_COMMON_TIMEOUT) -> "BaseElement":
        self._get_locator().fill(value, timeout=timeout)
        return self

    def press(self, key: str, timeout: int = OP_COMMON_TIMEOUT) -> "BaseElement":
        self._get_locator().press(key, timeout=timeout)
        return self

    def check(self, timeout: int = OP_COMMON_TIMEOUT, force: bool = False) -> "BaseElement":
        self._get_locator().check(timeout=timeout, force=force)
        return self

    def uncheck(self, timeout: int = OP_COMMON_TIMEOUT, force: bool = False) -> "BaseElement":
        self._get_locator().uncheck(timeout=timeout, force=force)
        return self

    def get_text(self) -> str:
        return self._get_locator().text_content() or ""

    def should_have_text(self, text: str, exact: bool = False) -> "BaseElement":
        expect(self._get_locator()).to_have_text(text, exact=exact)
        return self

    def should_be_enabled(self, enabled: bool = True) -> "BaseElement":
        expect(self._get_locator()).to_be_enabled(enabled=enabled)
        return self

    def should_be_disabled(self) -> "BaseElement":
        return self.should_be_enabled(enabled=False)

    def should_have_count(self, count: int) -> "BaseElement":
        expect(self._get_locator()).to_have_count(count)
        return self

    def wait_for(self, timeout: int = OP_COMMON_TIMEOUT) -> "BaseElement":
        self._get_locator().wait_for(timeout=timeout)
        return self

    def get_child_locator(self, locator: str) -> "BaseElement":
        return self.chain(BaseElement(By.LOCATOR, locator))


Element = BaseElement
