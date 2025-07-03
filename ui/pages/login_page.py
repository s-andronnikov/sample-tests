from common.decorators import ui_url
from common.routes import UIRoutes
from framework.ui.element import By, Element
from ui.pages.base_page import BasePage


@ui_url(UIRoutes.LOGIN)
class LoginPage(BasePage):
    el_login = Element(By.LOCATOR, "input[name='emailAddress']")
    el_password = Element(By.LOCATOR, "input[name='password']")
    el_login_btn = Element(By.LOCATOR, "button[id='st-loginButton']")

    error_toast = Element(By.LOCATOR, ".Toastify__toast--error")

    def login(self, login: str, password: str):
        self.el_login.fill(login)
        self.el_password.fill(password)
        self.el_login_btn.click()

        return self

    def should_see_error_toast(self, expected_message):
        self.error_toast.should_be_visible()
        message_span = self.error_toast.get_child_locator('span:has-text("' + expected_message + '")')

        assert message_span.should_be_visible(), f"Error toast with message '{expected_message}' not found"
