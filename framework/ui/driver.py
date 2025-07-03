from playwright.sync_api import Browser, BrowserType, Page, ViewportSize
from typing import Dict, List, Optional, Union, Any
from pathlib import Path

from playwright.sync_api import Browser, BrowserType, Page, BrowserContext

from config import base_settings


class Driver:
    browser: Optional[Browser] = None
    contexts: Dict[str, Dict[str, Any]] = {}
    current_context: Optional[str] = None
    auth_state_path: Path = Path('.auth/auth_state.json')

    @classmethod
    def init_browser(cls, browser: BrowserType) -> None:
        """Initialize browser instance"""
        cls.browser = browser.launch(
            channel="chrome",
            headless=base_settings.headless_mode,
            slow_mo=300 if base_settings.demo_test else None,
            args=("--start-maximized", '--lang=en-US')
        )

    @classmethod
    def new_workspace(cls) -> None:
        """Create a new browser context and page"""
        if cls.browser:
            new_context = cls.browser.new_context(
                ignore_https_errors=True,
                locale="en-US",
                viewport=ViewportSize(width=1920, height=1080),
                timezone_id="America/New_York",
                storage_state=cls.auth_state_path if cls.auth_state_path.exists() else None,
            )
            new_context.set_default_timeout(base_settings.timeout)

            if cls.contexts:
                # Create new context name by incrementing the last one (1-9)
                new_context_name = (
                    f"context_{int(tuple(cls.contexts.keys())[-1][-1])+1}"
                )
            else:
                new_context_name = "context_1"

            page = new_context.new_page()
            cls.contexts[new_context_name] = {
                "context": new_context,
                "pages": [page],
                "selected_page": 1,
            }
            cls.current_context = new_context_name
        else:
            raise Exception("Browser not initialized. Call init_browser first.")

    @classmethod
    def _get_current_context_payload(cls) -> Dict[str, Any]:
        """Get the current context data"""
        if cls.current_context is None:
            raise ValueError("No context selected")
        return cls.contexts[cls.current_context]

    @classmethod
    def get_driver(cls) -> Page:
        """Get the current page"""
        if cls.current_context is None:
            raise ValueError(
                "Driver is not initialized, call Driver.new_workspace first."
            )
        context = cls._get_current_context_payload()
        return context["pages"][context["selected_page"] - 1]

    @classmethod
    def close_contexts(cls) -> None:
        """Close all browser contexts"""
        for context_name, context_data in cls.contexts.items():
            context_data["context"].close()
        cls.contexts = {}
        cls.current_context = None

    @classmethod
    def close_browser(cls) -> None:
        """Close the browser instance"""
        if cls.browser:
            cls.browser.close()
            cls.browser = None

    @classmethod
    def new_page(cls) -> Page:
        """Create a new page in the current context"""
        if cls.current_context is None:
            raise ValueError("No context selected")

        context_data = cls._get_current_context_payload()
        context: BrowserContext = context_data["context"]
        page = context.new_page()
        context_data["pages"].append(page)
        context_data["selected_page"] = len(context_data["pages"])
        return page

    @classmethod
    def goto(cls, url: str) -> None:
        """Navigate to the specified URL"""
        cls.get_driver().goto(url)

    @classmethod
    def set_auth_state(cls, auth_state: dict) -> None:
        """Save authentication state"""
        cls.auth_state_path.parent.mkdir(exist_ok=True)
        cls.get_driver().context.storage_state(path=cls.auth_state_path)
