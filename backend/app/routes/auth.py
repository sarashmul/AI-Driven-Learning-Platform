"""
Authentication API routes for user registration, login, and profile management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging

from ..core.database import get_db
from ..core.auth import get_current_user
from ..models.user import User
from ..schemas.auth import (
    LoginRequest,
    RegisterRequest,
    LoginResponse,
    LogoutResponse,
    TokenResponse
)
from ..schemas.user import UserResponse, UserUpdate, PasswordChange
from ..services.auth_service import AuthService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", response_model=Dict[str, Any])
async def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """Register a new user account."""
    try:
        logger.info(f"Registration attempt for email: {user_data.email}")
        auth_service = AuthService(db)
        result = auth_service.register_user(user_data)
        logger.info(f"Registration successful for email: {user_data.email}")
        return result
    except Exception as e:
        logger.error(f"Registration failed for email: {user_data.email}, error: {str(e)}")
        raise


@router.post("/login", response_model=Dict[str, Any])
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Authenticate user and return access token."""
    auth_service = AuthService(db)
    result = auth_service.authenticate_user(login_data)
    return result


@router.post("/logout", response_model=LogoutResponse)
async def logout(current_user: User = Depends(get_current_user)):
    """Logout current user (client-side token removal)."""
    return LogoutResponse(message="Successfully logged out")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information."""
    return UserResponse.model_validate(current_user)


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile information."""
    auth_service = AuthService(db)
    updated_user = auth_service.update_user_profile(current_user.id, update_data)
    return UserResponse.model_validate(updated_user)


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change current user's password."""
    auth_service = AuthService(db)
    success = auth_service.change_password(
        current_user.id,
        password_data.current_password,
        password_data.new_password
    )
    
    if success:
        return {"message": "Password changed successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )


@router.get("/verify-token")
async def verify_token(current_user: User = Depends(get_current_user)):
    """Verify if the current token is valid."""
    return {
        "valid": True,
        "user_id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }
