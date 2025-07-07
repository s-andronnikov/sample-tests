class APIRoutes:
    """API route constants"""

    BASE = "/api"

    # Auth routes
    LOGIN = f"{BASE}/auth/login"
    REGISTER = f"{BASE}/auth/register"
    REFRESH_TOKEN = f"{BASE}/auth/refresh"

    # User routes
    USERS = f"{BASE}/users"
    USER_BY_ID = f"{BASE}/users/{{}}"

    # Contact routes
    CONTACTS = f"{BASE}/contacts"
    CONTACT_BY_ID = f"{BASE}/contacts/{{}}"


class UIRoutes:
    """UI route constants"""

    # Auth routes
    LOGIN = "login"
    REGISTER = "/register"

    # User routes
    USERS = "/users"
    USER_DETAILS = "/users/{}"

    # Contact routes
    CONTACTS = "/contacts"
    CONTACT_DETAILS = "/contacts/{}"

    # Dashboard
    DASHBOARD = "/dashboard"

    ASSET_CLASS = "/depreciation/9aa52b3f-f76d-438d-9557-92984bd9e1fc/configurations/asset-class"
