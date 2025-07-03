from typing import Any, Dict, List, Optional
from faker import Faker

from common.models import Contact, User

# Initialize Faker
fake = Faker()


class DataFactory:
    """Factory for generating test data"""

    @staticmethod
    def create_user(overrides: Dict[str, Any] = None) -> User:
        """Create a user with random data"""
        user_data = {
            "id": fake.random_int(min=1, max=100000),
            "username": fake.user_name(),
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "password": fake.password(length=12),
            "phone": fake.phone_number(),
            "is_active": True,
            "created_at": fake.date_time_this_year().isoformat(),
        }

        if overrides:
            user_data.update(overrides)

        return User(**user_data)

    @staticmethod
    def create_contact(overrides: Dict[str, Any] = None) -> Contact:
        """Create a contact with random data"""
        contact_data = {
            "id": fake.random_int(min=1, max=100000),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address(),
            "notes": fake.text(max_nb_chars=100),
            "created_at": fake.date_time_this_year().isoformat(),
            "user_id": fake.random_int(min=1, max=100),
        }

        if overrides:
            contact_data.update(overrides)

        return Contact(**contact_data)

    @staticmethod
    def create_multiple_users(count: int, overrides: Dict[str, Any] = None) -> List[User]:
        """Create multiple users with random data"""
        return [DataFactory.create_user(overrides) for _ in range(count)]

    @staticmethod
    def create_multiple_contacts(count: int, overrides: Dict[str, Any] = None) -> List[Contact]:
        """Create multiple contacts with random data"""
        return [DataFactory.create_contact(overrides) for _ in range(count)]

    @staticmethod
    def create_related_contacts(user_id: int, count: int) -> List[Contact]:
        """Create multiple contacts related to a specific user"""
        return DataFactory.create_multiple_contacts(count, {"user_id": user_id})
