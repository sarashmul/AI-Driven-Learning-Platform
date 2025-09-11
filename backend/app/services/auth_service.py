"""
Authentication service for user registration, login, and account management.
Handles user authentication, password management, and JWT token operations.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..schemas.auth import LoginRequest, RegisterRequest
from ..utils.security import hash_password, verify_password
from ..core.auth import create_token_for_user
from ..core.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
    ValidationException
)
from ..utils.validators import validate_email_format, validate_phone_number, validate_name
import logging

logger = logging.getLogger(__name__)


class AuthService:
    """Service for handling user authentication and account management."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def register_user(self, user_data: RegisterRequest) -> Dict[str, Any]:
        """
        Register a new user account.
        
        Args:
            user_data: User registration data
            
        Returns:
            Dictionary with user info and access token
            
        Raises:
            UserAlreadyExistsException: If email already exists
            ValidationException: If validation fails
        """
        # Validate input data
        self._validate_user_data(user_data.name, user_data.email, user_data.phone)
        
        # Check if user already exists
        existing_user = self.db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise UserAlreadyExistsException(user_data.email)
        
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Create new user
        new_user = User(
            name=user_data.name.strip(),
            email=user_data.email.lower(),
            phone=user_data.phone,
            password_hash=hashed_password,
            role="user",
            is_active=True,
            created_at=datetime.utcnow()
        )
        
        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            
            # Generate access token
            access_token = create_token_for_user(new_user)
            
            logger.info(f"New user registered: {new_user.email}")
            
            return {
                "user": new_user.to_dict(),
                "access_token": access_token,
                "token_type": "bearer",
                "message": "User registered successfully"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to register user {user_data.email}: {e}")
            raise ValidationException("Failed to create user account")
    
    def authenticate_user(self, login_data: LoginRequest) -> Dict[str, Any]:
        """
        Authenticate user login.
        
        Args:
            login_data: User login credentials
            
        Returns:
            Dictionary with user info and access token
            
        Raises:
            InvalidCredentialsException: If credentials are invalid
        """
        # Find user by email
        user = self.db.query(User).filter(
            User.email == login_data.email.lower(),
            User.is_active == True
        ).first()
        
        if not user:
            raise InvalidCredentialsException()
        
        # Verify password
        if not verify_password(login_data.password, user.password_hash):
            raise InvalidCredentialsException()
        
        # Update last login
        user.last_login = datetime.utcnow()
        
        try:
            self.db.commit()
            
            # Generate access token
            access_token = create_token_for_user(user)
            
            logger.info(f"User logged in: {user.email}")
            
            return {
                "user": user.to_dict(),
                "access_token": access_token,
                "token_type": "bearer",
                "message": "Login successful"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to update login time for {user.email}: {e}")
            # Still return success as authentication worked
            access_token = create_token_for_user(user)
            return {
                "user": user.to_dict(),
                "access_token": access_token,
                "token_type": "bearer",
                "message": "Login successful"
            }
    
    def get_user_by_id(self, user_id: int) -> User:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User object
            
        Raises:
            UserNotFoundException: If user not found
        """
        user = self.db.query(User).filter(
            User.id == user_id,
            User.is_active == True
        ).first()
        
        if not user:
            raise UserNotFoundException()
        
        return user
    
    def update_user_profile(self, user_id: int, update_data: UserUpdate) -> User:
        """
        Update user profile information.
        
        Args:
            user_id: User ID
            update_data: Updated user data
            
        Returns:
            Updated user object
            
        Raises:
            UserNotFoundException: If user not found
            ValidationException: If validation fails
        """
        user = self.get_user_by_id(user_id)
        
        # Validate update data
        if update_data.name:
            is_valid, error = validate_name(update_data.name)
            if not is_valid:
                raise ValidationException(error)
            user.name = update_data.name.strip()
        
        if update_data.phone is not None:
            is_valid, error = validate_phone_number(update_data.phone)
            if not is_valid:
                raise ValidationException(error)
            user.phone = update_data.phone
        
        user.updated_at = datetime.utcnow()
        
        try:
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"User profile updated: {user.email}")
            return user
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to update user profile {user_id}: {e}")
            raise ValidationException("Failed to update user profile")
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """
        Change user password.
        
        Args:
            user_id: User ID
            current_password: Current password
            new_password: New password
            
        Returns:
            True if password changed successfully
            
        Raises:
            UserNotFoundException: If user not found
            InvalidCredentialsException: If current password is wrong
            ValidationException: If new password is invalid
        """
        user = self.get_user_by_id(user_id)
        
        # Verify current password
        if not verify_password(current_password, user.password_hash):
            raise InvalidCredentialsException()
        
        # Hash new password
        try:
            new_password_hash = hash_password(new_password)
            user.password_hash = new_password_hash
            user.updated_at = datetime.utcnow()
            
            self.db.commit()
            
            logger.info(f"Password changed for user: {user.email}")
            return True
            
        except ValueError as e:
            raise ValidationException(str(e))
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to change password for user {user_id}: {e}")
            raise ValidationException("Failed to change password")
    
    def deactivate_user(self, user_id: int) -> bool:
        """
        Deactivate user account.
        
        Args:
            user_id: User ID
            
        Returns:
            True if user deactivated successfully
            
        Raises:
            UserNotFoundException: If user not found
        """
        user = self.get_user_by_id(user_id)
        
        user.is_active = False
        user.updated_at = datetime.utcnow()
        
        try:
            self.db.commit()
            logger.info(f"User deactivated: {user.email}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to deactivate user {user_id}: {e}")
            return False
    
    def _validate_user_data(self, name: str, email: str, phone: Optional[str] = None):
        """
        Validate user input data.
        
        Args:
            name: User name
            email: User email
            phone: User phone (optional)
            
        Raises:
            ValidationException: If validation fails
        """
        # Validate name
        is_valid, error = validate_name(name)
        if not is_valid:
            raise ValidationException(error)
        
        # Validate email
        is_valid, error = validate_email_format(email)
        if not is_valid:
            raise ValidationException(error)
        
        # Validate phone if provided
        if phone:
            is_valid, error = validate_phone_number(phone)
            if not is_valid:
                raise ValidationException(error)
