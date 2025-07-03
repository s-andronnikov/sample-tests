import pytest
from faker import Faker

from common.data_factory import DataFactory
from common.models import Contact

# Initialize Faker
fake = Faker()


@pytest.mark.api
@pytest.mark.skip(reason="Not implemented yet")
class TestContactAPI:
    """API tests for the contacts endpoints"""

    @pytest.mark.smoke
    def test_get_contacts(self, authenticated_api_client):
        """Test that authenticated users can get the list of contacts"""
        # Arrange & Act
        response = authenticated_api_client.get_contacts()

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert isinstance(data["items"], list)

    def test_get_contact_by_id(self, authenticated_api_client, test_contact):
        """Test that authenticated users can get a specific contact by ID"""
        # Arrange & Act
        response = authenticated_api_client.get_contact(test_contact["id"])

        # Assert
        assert response.status_code == 200
        contact = response.json()
        assert contact["id"] == test_contact["id"]
        assert contact["first_name"] == test_contact["first_name"]
        assert contact["last_name"] == test_contact["last_name"]

    def test_create_contact(self, authenticated_api_client, test_user):
        """Test that authenticated users can create a new contact"""
        # Arrange
        contact = DataFactory.create_contact({"user_id": test_user["id"]})
        contact_data = contact.dict(exclude={"id"})

        # Act
        response = authenticated_api_client.create_contact(contact_data)

        # Assert
        assert response.status_code == 201
        created_contact = response.json()
        assert created_contact["first_name"] == contact.first_name
        assert created_contact["last_name"] == contact.last_name
        assert created_contact["email"] == contact.email
        assert created_contact["user_id"] == test_user["id"]

        # Cleanup
        authenticated_api_client.delete_contact(created_contact["id"])

    def test_update_contact(self, authenticated_api_client, test_contact):
        """Test that authenticated users can update an existing contact"""
        # Arrange
        update_data = {"email": fake.email(), "phone": fake.phone_number(), "notes": fake.text(max_nb_chars=100)}

        # Act
        response = authenticated_api_client.update_contact(test_contact["id"], update_data)

        # Assert
        assert response.status_code == 200
        updated_contact = response.json()
        assert updated_contact["email"] == update_data["email"]
        assert updated_contact["phone"] == update_data["phone"]
        assert updated_contact["notes"] == update_data["notes"]

    def test_delete_contact(self, authenticated_api_client, test_user):
        """Test that authenticated users can delete a contact"""
        # Arrange - Create a contact to delete
        contact = DataFactory.create_contact({"user_id": test_user["id"]})
        create_response = authenticated_api_client.create_contact(contact.dict(exclude={"id"}))
        assert create_response.status_code == 201
        created_contact = create_response.json()

        # Act
        delete_response = authenticated_api_client.delete_contact(created_contact["id"])

        # Assert
        assert delete_response.status_code == 204

        # Verify the contact is deleted
        get_response = authenticated_api_client.get_contact(created_contact["id"])
        assert get_response.status_code == 404

    def test_filter_contacts_by_user(self, authenticated_api_client, test_user):
        """Test that contacts can be filtered by user ID"""
        # Arrange - Create multiple contacts for the test user
        contacts = DataFactory.create_related_contacts(test_user["id"], 3)
        created_contacts = []

        for contact in contacts:
            response = authenticated_api_client.create_contact(contact.dict(exclude={"id"}))
            assert response.status_code == 201
            created_contacts.append(response.json())

        # Act - Get contacts filtered by user ID
        response = authenticated_api_client.get(f"contacts?user_id={test_user['id']}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) >= len(created_contacts)

        # All returned contacts should belong to the test user
        for contact in data["items"]:
            assert contact["user_id"] == test_user["id"]

        # Cleanup
        for contact in created_contacts:
            authenticated_api_client.delete_contact(contact["id"])

    def test_unauthorized_access(self, api_client):
        """Test that unauthenticated requests are rejected"""
        # Act & Assert - Try to access protected endpoints
        response = api_client.get_contacts()
        assert response.status_code == 401

        response = api_client.create_contact({"first_name": "Test"})
        assert response.status_code == 401
