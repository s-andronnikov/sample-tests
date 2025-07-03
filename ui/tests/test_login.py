import pytest
from faker import Faker

from ui.pages.login_page import LoginPage

fake = Faker()


@pytest.mark.ui
class TestLogin:
    @pytest.mark.asyncio
    async def test_failed_login(self, login_page: LoginPage):
        name, password = fake.name(), fake.password()

        await login_page.open()
        await login_page.login(name, password)

        await login_page.should_see_error_toast("Invalid username/email and/or password.")

    @pytest.mark.asyncio
    async def test_success_login(self, login_page: LoginPage):
        await login_page.open()
        await login_page.login("admin", "password")

        await login_page.should_be_redirected_from_login()
