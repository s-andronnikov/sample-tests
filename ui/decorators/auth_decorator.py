import functools
from enum import Enum, auto
from typing import TypeVar

from config import base_settings
from ui.pages.login_page import LoginPage


class UserRole(Enum):
    """User roles for authentication"""

    ADMIN = auto()
    USER = auto()
    READONLY = auto()


T = TypeVar("T")


def _get_credentials(role: UserRole) -> tuple[str, str]:
    """Get credentials for the specified role

    Args:
        role: The user role

    Returns:
        Tuple of (username, password)
    """
    if role == UserRole.ADMIN:
        return base_settings.admin_username, base_settings.admin_password
    elif role == UserRole.USER:
        return base_settings.user_username, base_settings.user_password
    elif role == UserRole.READONLY:
        return base_settings.readonly_username, base_settings.readonly_password
    else:
        raise ValueError(f"Unknown user role: {role}")


def with_auth(role: UserRole = UserRole.ADMIN):
    """Decorator to authenticate test classes with specified user role

    This decorator should be applied to test classes. It will login before
    running the test methods and ensure the user is authenticated.

    Args:
        role: The user role to authenticate with (default: ADMIN)

    Example:
        @with_auth(UserRole.ADMIN)
        class TestSomething:
            def test_something(self):
                # Test is run with admin user authenticated
                pass
    """

    def decorator(cls: type[T]) -> type[T]:
        # Store original setup method if it exists
        original_setup = getattr(cls, "setup_class", None)

        @functools.wraps(original_setup or (lambda dec_cls: None))
        def setup_with_auth(dec_cls):
            # Call original setup_class if it exists
            if original_setup:
                original_setup()

            # Perform login
            login_page = LoginPage()
            login_page.open()

            # Get credentials for the specified role
            username, password = _get_credentials(role)
            login_page.login(username, password)

            # Verify successful login
            login_page.should_be_redirected_from_login()

            # Store authenticated state on the class
            dec_cls._auth_role = role

        # Replace setup_class with our authenticated version
        cls.setup_class = setup_with_auth
        return cls

    return decorator
