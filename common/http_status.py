"""HTTP Status Code constants for use in API testing."""

# Import status codes from requests library
from requests import codes as status_codes

# Success codes
OK = status_codes.ok  # 200
CREATED = status_codes.created  # 201
ACCEPTED = status_codes.accepted  # 202
NO_CONTENT = status_codes.no_content  # 204

# Client error codes
BAD_REQUEST = status_codes.bad_request  # 400
UNAUTHORIZED = status_codes.unauthorized  # 401
FORBIDDEN = status_codes.forbidden  # 403
NOT_FOUND = status_codes.not_found  # 404

# Server error codes
SERVER_ERROR = status_codes.server_error  # 500
