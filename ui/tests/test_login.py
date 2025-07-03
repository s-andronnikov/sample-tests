import pytest
from faker.proxy import Faker

from ui.pages.login_page import LoginPage

fake = Faker()


@pytest.mark.ui
class TestLogin:
    def test_failed_login(self, login_page: LoginPage):
        name, password = fake.name(), fake.password()

        login_page.open()
        login_page.login(name, password)

        login_page.should_see_error_toast("Invalid username/email and/or password.")

    def test_success_login(self, login_page: LoginPage):
        login_page.open()
        login_page.login("admin", "password")

        login_page.should_be_redirected_from_login()
