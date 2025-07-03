import pytest
import pytest_asyncio
from faker import Faker

# Initialize Faker
fake = Faker()


@pytest.mark.ui
@pytest.mark.skip(reason="Not implemented yet")
class TestContacts:
    """UI tests for the contacts section"""

    @pytest.mark.smoke
    async def test_view_contacts(self, authenticated_contact_page):
        """Test that a user can view contacts"""
        # Arrange & Act
        await authenticated_contact_page.open()

        # Assert
        await authenticated_contact_page.title.should_be_visible()
        # Assuming we have at least one contact in the system
        assert await authenticated_contact_page.grid.rows.count() > 0

    async def test_add_contact(self, authenticated_contact_page):
        """Test that a user can add a new contact"""
        # Arrange
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"

        # Act
        await authenticated_contact_page.add_contact(
            first_name=first_name,
            last_name=last_name,
            email=fake.email(),
            phone=fake.phone_number(),
            address=fake.address(),
            notes=fake.text(max_nb_chars=100),
            user_id="1",  # Assuming user ID 1 exists
        )

        # Assert
        await authenticated_contact_page.should_see_contact(full_name)
        await authenticated_contact_page.alert.should_have_text(f"Contact {full_name} created successfully")

    async def test_edit_contact(self, authenticated_contact_page):
        """Test that a user can edit an existing contact"""
        # Arrange - Create a test contact
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"

        await authenticated_contact_page.add_contact(first_name=first_name, last_name=last_name)

        # New data for editing
        new_email = fake.email()

        # Act - Edit the contact
        await authenticated_contact_page.edit_contact(name=full_name, email=new_email)

        # Assert
        await authenticated_contact_page.alert.should_have_text(f"Contact {full_name} updated successfully")

        # Verify the change by opening contact details
        await authenticated_contact_page.view_contact_details(full_name)
        email_field = authenticated_contact_page.contact_dialog.email_input
        await email_field.should_have_text(new_email)

    async def test_delete_contact(self, authenticated_contact_page):
        """Test that a user can delete a contact"""
        # Arrange - Create a test contact
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"

        await authenticated_contact_page.add_contact(first_name=first_name, last_name=last_name)

        # Act - Delete the contact
        await authenticated_contact_page.delete_contact(full_name)

        # Assert
        await authenticated_contact_page.should_not_see_contact(full_name)
        await authenticated_contact_page.alert.should_have_text(f"Contact {full_name} deleted successfully")

    async def test_search_contact(self, authenticated_contact_page):
        """Test that a user can search for contacts"""
        # Arrange - Create a contact with a unique name
        unique_name = f"UniqueTest{fake.random_number(digits=5)}"
        full_name = f"{unique_name} {fake.last_name()}"

        await authenticated_contact_page.add_contact(first_name=unique_name, last_name=fake.last_name())

        # Act - Search for the contact
        await authenticated_contact_page.search_contact(unique_name)

        # Assert - Should see only this contact
        await authenticated_contact_page.should_see_contact(full_name)

        # The grid should have only one row (plus header)
        assert await authenticated_contact_page.grid.rows.count() == 1
