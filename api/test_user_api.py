import pytest
from faker import Faker

from common.data_factory import DataFactory
from common.models import User

# Initialize Faker
fake = Faker()


@pytest.mark.api
@pytest.mark.skip(reason="Not implemented yet")
class TestUserAPI:
    """API tests for the users endpoints"""

    @pytest.mark.smoke
    def test_login(self, api_client):
        """Test that a user can login via API"""
        # Arrange & Act
        response = api_client.login("admin", "adminpassword")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert data["user"]["username"] == "admin"

    def test_get_users(self, authenticated_api_client):
        """Test that authenticated users can get the list of users"""
        # Arrange & Act
        response = authenticated_api_client.get_users()

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert data["total"] > 0

    def test_get_user_by_id(self, authenticated_api_client, test_user):
        """Test that authenticated users can get a specific user by ID"""
        # Arrange & Act
        response = authenticated_api_client.get_user(test_user["id"])

        # Assert
        assert response.status_code == 200
        user = response.json()
        assert user["id"] == test_user["id"]
        assert user["username"] == test_user["username"]

    def test_create_user(self, authenticated_api_client):
        """Test that authenticated users can create a new user"""
        # Arrange
        user = DataFactory.create_user()
        user_data = user.dict(exclude={"id"})

        # Act
        response = authenticated_api_client.create_user(user_data)

        # Assert
        assert response.status_code == 201
        created_user = response.json()
        assert created_user["username"] == user.username
        assert created_user["email"] == user.email

        # Cleanup
        authenticated_api_client.delete_user(created_user["id"])

    def test_update_user(self, authenticated_api_client, test_user):
        """Test that authenticated users can update an existing user"""
        # Arrange
        update_data = {
            "email": fake.email(),
            "phone": fake.phone_number()
        }

        # Act
        response = authenticated_api_client.update_user(test_user["id"], update_data)

        # Assert
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["email"] == update_data["email"]
        assert updated_user["phone"] == update_data["phone"]

    def test_delete_user(self, authenticated_api_client):
        """Test that authenticated users can delete a user"""
        # Arrange - Create a user to delete
        user = DataFactory.create_user()
        create_response = authenticated_api_client.create_user(user.dict(exclude={"id"}))
        assert create_response.status_code == 201
        created_user = create_response.json()

        # Act
        delete_response = authenticated_api_client.delete_user(created_user["id"])

        # Assert
        assert delete_response.status_code == 204

        # Verify the user is deleted
        get_response = authenticated_api_client.get_user(created_user["id"])
        assert get_response.status_code == 404

    def test_unauthorized_access(self, api_client):
        """Test that unauthenticated requests are rejected"""
        # Act & Assert - Try to access protected endpoints
        response = api_client.get_users()
        assert response.status_code == 401

        response = api_client.create_user({"username": "test"})
        assert response.status_code == 401
