import json
from typing import Any, Dict, List, Optional, Union

import requests
from requests import Response

from config import base_settings
from common.routes import APIRoutes


class APIClient:
    """Client for interacting with the API"""

    def __init__(self, base_url: str = None, token: str = None):
        self.base_url = base_url or base_settings.api_base_url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if token:
            self.set_auth_token(token)

    def set_auth_token(self, token: str) -> None:
        """Set the authentication token for requests"""
        self.headers["Authorization"] = f"Bearer {token}"

    def _make_url(self, endpoint: str) -> str:
        """Create a full URL from the endpoint"""
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def get(self, endpoint: str, params: Dict[str, Any] = None) -> Response:
        """Make a GET request to the API"""
        url = self._make_url(endpoint)
        return requests.get(url, headers=self.headers, params=params)

    def post(self, endpoint: str, data: Dict[str, Any] = None) -> Response:
        """Make a POST request to the API"""
        url = self._make_url(endpoint)
        return requests.post(url, headers=self.headers, json=data)

    def put(self, endpoint: str, data: Dict[str, Any] = None) -> Response:
        """Make a PUT request to the API"""
        url = self._make_url(endpoint)
        return requests.put(url, headers=self.headers, json=data)

    def delete(self, endpoint: str) -> Response:
        """Make a DELETE request to the API"""
        url = self._make_url(endpoint)
        return requests.delete(url, headers=self.headers)

    # Convenience methods for specific API endpoints

    def login(self, username: str, password: str) -> Response:
        """Login to the API and get an authentication token"""
        response = self.post(APIRoutes.LOGIN, {
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            data = response.json()
            if "token" in data:
                self.set_auth_token(data["token"])

        return response

    def get_users(self) -> Response:
        """Get all users"""
        return self.get(APIRoutes.USERS)

    def get_user(self, user_id: int) -> Response:
        """Get a specific user"""
        return self.get(f"{APIRoutes.USERS}/{user_id}")

    def create_user(self, user_data: Dict[str, Any]) -> Response:
        """Create a new user"""
        return self.post(APIRoutes.USERS, user_data)

    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Response:
        """Update an existing user"""
        return self.put(f"{APIRoutes.USERS}/{user_id}", user_data)

    def delete_user(self, user_id: int) -> Response:
        """Delete a user"""
        return self.delete(f"{APIRoutes.USERS}/{user_id}")

    def get_contacts(self) -> Response:
        """Get all contacts"""
        return self.get(APIRoutes.CONTACTS)

    def get_contact(self, contact_id: int) -> Response:
        """Get a specific contact"""
        return self.get(f"{APIRoutes.CONTACTS}/{contact_id}")

    def create_contact(self, contact_data: Dict[str, Any]) -> Response:
        """Create a new contact"""
        return self.post(APIRoutes.CONTACTS, contact_data)

    def update_contact(self, contact_id: int, contact_data: Dict[str, Any]) -> Response:
        """Update an existing contact"""
        return self.put(f"{APIRoutes.CONTACTS}/{contact_id}", contact_data)

    def delete_contact(self, contact_id: int) -> Response:
        """Delete a contact"""
        return self.delete(f"{APIRoutes.CONTACTS}/{contact_id}")
