import pytest

from ui.decorators.auth_decorator import UserRole, with_auth


@pytest.mark.ui
@pytest.mark.skip(reason="Sample only")
@with_auth(UserRole.ADMIN)
class TestWithAdminAuth:
    """Example test class using admin authentication"""

    def test_admin_operation(self):
        """Test that requires admin privileges"""
        # This test will run with admin user already logged in
        assert True


@pytest.mark.ui
@pytest.mark.skip(reason="Sample only")
@with_auth(UserRole.USER)
class TestWithUserAuth:
    """Example test class using regular user authentication"""

    def test_user_operation(self):
        """Test that requires regular user privileges"""
        # This test will run with regular user already logged in
        assert True


@pytest.mark.ui
@pytest.mark.skip(reason="Sample only")
@with_auth(UserRole.READONLY)
class TestWithReadOnlyAuth:
    """Example test class using read-only user authentication"""

    def test_readonly_operation(self):
        """Test that requires read-only privileges"""
        # This test will run with read-only user already logged in
        assert True


@pytest.mark.ui
@pytest.mark.skip(reason="Sample only")
@with_auth()  # Default is ADMIN
class TestWithDefaultAuth:
    """Example test class using default authentication (admin)"""

    def test_default_auth(self):
        """Test with default auth (admin)"""
        # This test will run with admin user already logged in
        assert True
