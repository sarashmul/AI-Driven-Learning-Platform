"""
Authentication Pydantic schemas for login, registration, and token handling.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class LoginRequest(BaseModel):
    """Schema for user login requests."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class RegisterRequest(BaseModel):
    """Schema for user registration requests."""
    name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    phone: Optional[str] = Field(None, max_length=20, description="User's phone number")
    password: str = Field(..., min_length=8, description="User's password")


class TokenResponse(BaseModel):
    """Schema for authentication token responses."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class LoginResponse(BaseModel):
    """Schema for successful login responses."""
    user: dict = Field(..., description="User information")
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class LogoutResponse(BaseModel):
    """Schema for logout responses."""
    message: str = Field(default="Successfully logged out", description="Logout confirmation message")


class TokenValidationResponse(BaseModel):
    """Schema for token validation responses."""
    valid: bool = Field(..., description="Whether the token is valid")
    user_id: Optional[int] = Field(None, description="User ID if token is valid")
    expires_at: Optional[str] = Field(None, description="Token expiration time")


class PasswordResetRequest(BaseModel):
    """Schema for password reset requests."""
    email: EmailStr = Field(..., description="User's email address for password reset")


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation."""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, description="New password")


class RefreshTokenRequest(BaseModel):
    """Schema for token refresh requests."""
    refresh_token: str = Field(..., description="Refresh token")


class AuthStatusResponse(BaseModel):
    """Schema for authentication status responses."""
    authenticated: bool = Field(..., description="Whether user is authenticated")
    user: Optional[dict] = Field(None, description="User information if authenticated")
    role: Optional[str] = Field(None, description="User role if authenticated")
