import pytest
from faker.proxy import Faker

from config import base_settings
from ui.pages.login_page import LoginPage

fake = Faker()


@pytest.mark.ui
class TestLogin:
    def test_failed_login(self, login_page: LoginPage):
        name, password = fake.name(), fake.password()

        login_page.open()
        login_page.login(name, password, check_already_logged_in=False)

        login_page.should_see_error_toast("Invalid username/email and/or password.")

    def test_success_login(self, login_page: LoginPage):
        login_page.open()
        login_page.login(base_settings.admin_username, base_settings.admin_password, check_already_logged_in=False)

        login_page.should_be_redirected_from_login()
