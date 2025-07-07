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

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


base_settings = BaseConfig()
