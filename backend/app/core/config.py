"""
Application configuration settings using Pydantic for environment variable management.
Handles database, JWT, AI API, and other core settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "AI-Driven Learning Platform"
    debug: bool = False
    
    # Database - PostgreSQL by default for production
    database_url: str = "postgresql://postgres:password@localhost:5432/learning_platform"
    
    # JWT Authentication
    secret_key: str = "CHANGE-THIS-IN-PRODUCTION-USE-A-SECURE-RANDOM-KEY"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AI Configuration
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    
    # CORS - Add your production URLs here
    allowed_origins: list = [
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        # Add your production frontend URLs here
        # "https://your-frontend-domain.onrender.com",
        # "https://your-custom-domain.com"
    ]
    
    # Pagination
    default_page_size: int = 10
    max_page_size: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
