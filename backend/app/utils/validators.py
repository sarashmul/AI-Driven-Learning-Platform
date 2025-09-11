"""
Input validation utilities for API endpoints.
Provides common validation functions for user input.
"""
import re
from typing import Optional, List
from email_validator import validate_email, EmailNotValidError


def validate_email_format(email: str) -> tuple[bool, Optional[str]]:
    """
    Validate email format using email-validator library.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Validate and get normalized result
        valid = validate_email(email)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)


def validate_phone_number(phone: str) -> tuple[bool, Optional[str]]:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not phone:
        return True, None  # Phone is optional
    
    # Remove spaces, dashes, parentheses
    cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check if it contains only digits and plus sign
    if not re.match(r'^\+?[\d]{10,15}$', cleaned_phone):
        return False, "Phone number must contain 10-15 digits and may start with +"
    
    return True, None


def validate_name(name: str) -> tuple[bool, Optional[str]]:
    """
    Validate user name format.
    
    Args:
        name: Name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or len(name.strip()) == 0:
        return False, "Name is required"
    
    if len(name.strip()) < 2:
        return False, "Name must be at least 2 characters long"
    
    if len(name.strip()) > 100:
        return False, "Name must be less than 100 characters"
    
    # Allow letters, spaces, hyphens, apostrophes
    if not re.match(r"^[a-zA-Z\s\-']+$", name.strip()):
        return False, "Name can only contain letters, spaces, hyphens, and apostrophes"
    
    return True, None


def validate_category_name(name: str) -> tuple[bool, Optional[str]]:
    """
    Validate category/subcategory name format.
    
    Args:
        name: Category name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or len(name.strip()) == 0:
        return False, "Category name is required"
    
    if len(name.strip()) < 2:
        return False, "Category name must be at least 2 characters long"
    
    if len(name.strip()) > 100:
        return False, "Category name must be less than 100 characters"
    
    # Allow letters, numbers, spaces, hyphens
    if not re.match(r"^[a-zA-Z0-9\s\-]+$", name.strip()):
        return False, "Category name can only contain letters, numbers, spaces, and hyphens"
    
    return True, None


def validate_prompt_text(prompt: str) -> tuple[bool, Optional[str]]:
    """
    Validate prompt text format and length.
    
    Args:
        prompt: Prompt text to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not prompt or len(prompt.strip()) == 0:
        return False, "Prompt text is required"
    
    if len(prompt.strip()) < 10:
        return False, "Prompt must be at least 10 characters long"
    
    if len(prompt.strip()) > 2000:
        return False, "Prompt must be less than 2000 characters"
    
    return True, None


def sanitize_input(text: str) -> str:
    """
    Sanitize user input by removing dangerous characters.
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove potential script tags and dangerous characters
    sanitized = re.sub(r'<script.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    sanitized = re.sub(r'<.*?>', '', sanitized)  # Remove HTML tags
    
    return sanitized.strip()


def validate_pagination_params(page: int, size: int, max_size: int = 100) -> tuple[bool, Optional[str]]:
    """
    Validate pagination parameters.
    
    Args:
        page: Page number (1-based)
        size: Page size
        max_size: Maximum allowed page size
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if page < 1:
        return False, "Page number must be greater than 0"
    
    if size < 1:
        return False, "Page size must be greater than 0"
    
    if size > max_size:
        return False, f"Page size cannot exceed {max_size}"
    
    return True, None
