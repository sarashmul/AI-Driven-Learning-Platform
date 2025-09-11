"""
JWT authentication utilities for token generation and verification.
Handles user authentication, token creation, and security.
"""
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from ..models.user import User

# Security scheme for Bearer token
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with optional expiration time.
    
    Args:
        data: The payload data to encode in the token
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    
    try:
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create access token"
        )


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token string to verify
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        print(f"🔐 DEBUG: Token payload: {payload}")
        return payload
    except JWTError as e:
        print(f"❌ DEBUG: JWT Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from JWT token.
    
    Args:
        credentials: Bearer token credentials
        db: Database session
        
    Returns:
        Current authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    print(f"🔐 DEBUG: Received credentials: {credentials}")
    print(f"🔐 DEBUG: Token: {credentials.credentials[:20]}..." if credentials.credentials else "NO TOKEN")
    
    token = credentials.credentials
    payload = verify_token(token)
    
    print(f"🔐 DEBUG: Token payload: {payload}")
    
    # Extract user ID from token payload
    user_id_raw = payload.get("sub")
    if user_id_raw is None:
        print(f"❌ DEBUG: No 'sub' field in token payload")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload - missing sub"
        )
    
    # Convert to int if it's a string
    try:
        user_id = int(user_id_raw)
        print(f"🔐 DEBUG: Converted user_id: {user_id} (type: {type(user_id)})")
    except (ValueError, TypeError) as e:
        print(f"❌ DEBUG: Could not convert user_id '{user_id_raw}' to int: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload - invalid user ID"
        )
    
    # Get user from database
    print(f"🔐 DEBUG: Querying database for user_id: {user_id}")
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    print(f"🔐 DEBUG: Found user: {user.email if user else 'None'}")
    
    if user is None:
        print(f"❌ DEBUG: User not found in database or inactive")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    return user


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current authenticated admin user.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current admin user
        
    Raises:
        HTTPException: If user is not an admin
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin access required."
        )
    
    return current_user


def create_token_for_user(user: User) -> str:
    """
    Create an access token for a specific user.
    
    Args:
        user: User object to create token for
        
    Returns:
        JWT access token
    """
    token_data = {
        "sub": str(user.id),  # Convert to string for JWT standard compliance
        "email": user.email,
        "role": user.role
    }
    return create_access_token(data=token_data)
