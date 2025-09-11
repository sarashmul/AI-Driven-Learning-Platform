"""
Security utilities for password hashing and verification.
Uses bcrypt for secure password handling.
"""
from passlib.context import CryptContext
from typing import Union

# Configure password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to verify against
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def is_password_strong(password: str) -> tuple[bool, list[str]]:
    """
    Check if a password meets strength requirements.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    # Check length
    if len(password) < 8:
        issues.append("Password must be at least 8 characters long")
    
    # Check for uppercase
    if not any(c.isupper() for c in password):
        issues.append("Password must contain at least one uppercase letter")
    
    # Check for lowercase
    if not any(c.islower() for c in password):
        issues.append("Password must contain at least one lowercase letter")
    
    # Check for numbers
    if not any(c.isdigit() for c in password):
        issues.append("Password must contain at least one number")
    
    # Check for special characters
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        issues.append("Password must contain at least one special character")
    
    return len(issues) == 0, issues


def generate_password_hash(password: str) -> str:
    """
    Generate a secure hash for a password with validation.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
        
    Raises:
        ValueError: If password doesn't meet requirements
    """
    is_valid, issues = is_password_strong(password)
    if not is_valid:
        raise ValueError(f"Password validation failed: {', '.join(issues)}")
    
    return hash_password(password)
