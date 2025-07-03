from collections.abc import Generator

import pytest

from common.api_client import APIClient
from common.data_factory import DataFactory
from common.db_client import DBClient
from common.http_status import CREATED, OK


@pytest.fixture
def api_client() -> APIClient:
    """Return an APIClient instance"""
    return APIClient()


@pytest.fixture
def db_client() -> Generator[DBClient, None, None]:
    """Return a DBClient instance and close it after the test"""
    client = DBClient()
    yield client
    client.close()


@pytest.fixture
def authenticated_api_client() -> APIClient:
    """Return an authenticated APIClient instance"""
    client = APIClient()
    response = client.login("admin", "adminpassword")
    assert response.status_code == OK, f"Authentication failed: {response.text}"
    return client


@pytest.fixture
def test_user(authenticated_api_client):
    """Create a test user and return it"""
    # Create a user with random data
    user = DataFactory.create_user()
    response = authenticated_api_client.create_user(user.dict(exclude={"id"}))
    assert response.status_code == CREATED, f"Failed to create test user: {response.text}"

    created_user = response.json()

    # Cleanup after test
    yield created_user

    authenticated_api_client.delete_user(created_user["id"])


@pytest.fixture
def test_contact(authenticated_api_client, test_user):
    """Create a test contact and return it"""
    # Create a contact with random data linked to the test user
    contact = DataFactory.create_contact({"user_id": test_user["id"]})
    response = authenticated_api_client.create_contact(contact.dict(exclude={"id"}))
    assert response.status_code == CREATED, f"Failed to create test contact: {response.text}"

    created_contact = response.json()

    # Cleanup after test
    yield created_contact

    authenticated_api_client.delete_contact(created_contact["id"])
