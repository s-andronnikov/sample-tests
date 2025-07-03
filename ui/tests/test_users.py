import pytest
from faker import Faker

# Initialize Faker
fake = Faker()


@pytest.mark.ui
@pytest.mark.skip(reason="Not implemented yet")
class TestUsers:
    """UI tests for the users section"""

    @pytest.mark.smoke
    async def test_login(self, user_page):
        """Test that a user can log in successfully"""
        # Arrange
        await user_page.open()

        # Act
        await user_page.login("admin", "adminpassword")

        # Assert
        await user_page.title.should_be_visible()
        await user_page.should_see_user("admin")

    def test_add_user(self, authenticated_user_page):
        """Test that a user can add a new user"""
        # Arrange
        username = fake.user_name()
        email = fake.email()
        first_name = fake.first_name()
        last_name = fake.last_name()

        # Act
        authenticated_user_page.add_user(
            username=username, email=email, first_name=first_name, last_name=last_name, password=fake.password(), phone=fake.phone_number()
        )

        # Assert
        authenticated_user_page.should_see_user(username)
        authenticated_user_page.alert.should_have_text(f"User {username} created successfully")

    def test_edit_user(self, authenticated_user_page):
        """Test that a user can edit an existing user"""
        # Arrange - Create a test user
        username = fake.user_name()
        authenticated_user_page.add_user(username=username)

        # New data for editing
        new_email = fake.email()

        # Act - Edit the user
        authenticated_user_page.edit_user(username=username, email=new_email)

        # Assert
        authenticated_user_page.alert.should_have_text(f"User {username} updated successfully")

        # Verify the change by opening user details
        authenticated_user_page.get_user_row(username).click()
        email_field = authenticated_user_page.user_dialog.email_input
        email_field.should_have_text(new_email)

    def test_delete_user(self, authenticated_user_page):
        """Test that a user can delete a user"""
        # Arrange - Create a test user
        username = fake.user_name()
        authenticated_user_page.add_user(username=username)

        # Act - Delete the user
        authenticated_user_page.delete_user(username)

        # Assert
        authenticated_user_page.should_not_see_user(username)
        authenticated_user_page.alert.should_have_text(f"User {username} deleted successfully")

    def test_search_user(self, authenticated_user_page):
        """Test that a user can search for users"""
        # Arrange - Create a user with a unique name
        unique_name = f"UniqueTest{fake.random_number(digits=5)}"
        authenticated_user_page.add_user(username=unique_name, first_name=unique_name, last_name=fake.last_name())

        # Act - Search for the user
        authenticated_user_page.search_user(unique_name)

        # Assert - Should see only this user
        authenticated_user_page.should_see_user(unique_name)

        # The grid should have only one row (plus header)
        assert authenticated_user_page.grid.rows.count() == 1
