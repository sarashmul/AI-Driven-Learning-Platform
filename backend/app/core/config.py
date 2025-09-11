"""
Application configuration settings using Pydantic for environment variable management.
Handles database, JWT, AI API, and other core settings.
"""
from pydantic_settings import BaseSettings
from pydantic import validator
from typing import Optional, List, Union
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "AI-Driven Learning Platform"
    debug: bool = False
    
    # Database - PostgreSQL with psycopg3 for production
    # Will use DATABASE_URL from environment variables (Render) or fallback to local
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:password@localhost:5433/learning_platform")
    # JWT Authentication
    secret_key: str = "CHANGE-THIS-IN-PRODUCTION-USE-A-SECURE-RANDOM-KEY"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AI Configuration
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    
    # CORS - Add your production URLs here
    # allowed_origins: list = [
    #     "http://localhost:3000", 
    #     "http://127.0.0.1:3000",
    #     "http://localhost:5173",
    #     "http://127.0.0.1:5173",
    #     # Add your production frontend URLs here
    #     # "https://your-frontend-domain.onrender.com",
    #     # "https://your-custom-domain.com"
    # ]
    allowed_origins: Union[str, List[str]] = [
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    
    @validator('allowed_origins', pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list format."""
        if isinstance(v, str):
             # Split by comma and clean whitespace
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    @validator('database_url', pre=True)
    def ensure_psycopg_format(cls, v):
        """
        Ensure database URL uses psycopg (not psycopg2) for SQLAlchemy compatibility.
        Render provides postgresql:// but we need postgresql+psycopg:// for psycopg3.
        """
        if isinstance(v, str) and v.startswith('postgresql://'):
            # Convert postgresql:// to postgresql+psycopg:// for SQLAlchemy
            return v.replace('postgresql://', 'postgresql+psycopg://', 1)
        return v
    # Pagination
    default_page_size: int = 10
    max_page_size: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
