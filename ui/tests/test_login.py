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

    # def test_success_login(self, login_page: LoginPage):
    #     login_page.open()
    #     login_page.login("user", "password")

        # login_page.title.should_be_visible()
        # login_page.should_see_user("admin")
