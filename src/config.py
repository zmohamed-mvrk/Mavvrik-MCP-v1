import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    api_url: str = Field("https://graphql.mavvrik.dev", alias="MAVVRIK_API_URL")
    
    # Auth (Optional to prevent startup crashes)
    dev_api_key: Optional[str] = Field(default=None, alias="MAVVRIK_API_KEY")
    dev_tenant_id: Optional[str] = Field(default=None, alias="MAVVRIK_TENANT_ID")

    # Guardrails & Timeouts
    max_list_limit: int = 20 
    request_timeout: float = 30.0 
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore" 

settings = Settings()