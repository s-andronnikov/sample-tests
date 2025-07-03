from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

USERNAME_MIN_LENGTH = 3

class User(BaseModel):
    """User model for API and database interactions"""

    id: int | None = None
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str | None = None
    phone: str | None = None
    is_active: bool = True
    created_at: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("username")
    def username_must_be_valid(self, v):
        if len(v) < USERNAME_MIN_LENGTH:
            raise ValueError("Username must be at least 3 characters")
        return v

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Contact(BaseModel):
    """Contact model for API and database interactions"""

    id: int | None = None
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    address: str | None = None
    notes: str | None = None
    created_at: str | None = None
    user_id: int

    model_config = ConfigDict(from_attributes=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class LoginRequest(BaseModel):
    """Login request model"""

    username: str
    password: str


class LoginResponse(BaseModel):
    """Login response model"""

    token: str
    user: User


class APIError(BaseModel):
    """API error response model"""

    detail: str
    status_code: int


class PaginatedResponse(BaseModel):
    """Generic paginated response model"""

    items: list[User | Contact]
    total: int
    page: int
    size: int
    pages: int
