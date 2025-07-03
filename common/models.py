from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class User(BaseModel):
    """User model for API and database interactions"""
    id: Optional[int] = None
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    password: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True
    created_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("username")
    def username_must_be_valid(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        return v

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Contact(BaseModel):
    """Contact model for API and database interactions"""
    id: Optional[int] = None
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    address: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None
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
    items: List[Union[User, Contact]]
    total: int
    page: int
    size: int
    pages: int
