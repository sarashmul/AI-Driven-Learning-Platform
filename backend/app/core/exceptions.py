"""
Custom exception classes for the application.
Provides specific exceptions for different error scenarios.
"""
from fastapi import HTTPException, status


class UserAlreadyExistsException(HTTPException):
    """Raised when trying to create a user with an existing email."""
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {email} already exists"
        )


class UserNotFoundException(HTTPException):
    """Raised when a user is not found."""
    def __init__(self, identifier: str = "User"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{identifier} not found"
        )


class InvalidCredentialsException(HTTPException):
    """Raised when login credentials are invalid."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


class CategoryNotFoundException(HTTPException):
    """Raised when a category is not found."""
    def __init__(self, category_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found"
        )


class SubCategoryNotFoundException(HTTPException):
    """Raised when a subcategory is not found."""
    def __init__(self, subcategory_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"SubCategory with ID {subcategory_id} not found"
        )


class PromptNotFoundException(HTTPException):
    """Raised when a prompt is not found."""
    def __init__(self, prompt_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prompt with ID {prompt_id} not found"
        )


class AIServiceException(HTTPException):
    """Raised when AI service encounters an error."""
    def __init__(self, detail: str = "AI service temporarily unavailable"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail
        )


class DatabaseException(HTTPException):
    """Raised when database operations fail."""
    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class ValidationException(HTTPException):
    """Raised when input validation fails."""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )


class PermissionDeniedException(HTTPException):
    """Raised when user doesn't have required permissions."""
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )
