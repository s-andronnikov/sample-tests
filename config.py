from pydantic import Field
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    protocol: str = Field("http", description="Protocol used for requests")
    domain: str = Field("localhost", description="Domain name")
    host: str = Field("localhost:8000", description="Host address")
    api_base_url: str = Field("http://localhost:8000/api", description="Base URL for API requests")
    db_url: str = Field("postgresql://user:password@localhost:5432/testdb", description="Database connection string")
    headless_mode: bool = Field(True, description="Run browser in headless mode")
    demo_test: bool = Field(False, description="Run tests in demo mode")
    timeout: int = Field(10000, description="Default timeout in milliseconds")
    depreciation_id: str = Field("9aa52b3f-f76d-438d-9557-92984bd9e1fc", description="Depreciation ID for asset class tests")

    # User credentials for testing
    admin_username: str = Field("admin", description="Admin username for testing")
    admin_password: str = Field("password", description="Admin password for testing")
    user_username: str = Field("user", description="Regular user username for testing")
    user_password: str = Field("userpass", description="Regular user password for testing")
    readonly_username: str = Field("readonly", description="Read-only user username for testing")
    readonly_password: str = Field("readonlypass", description="Read-only user password for testing")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


base_settings = BaseConfig()
