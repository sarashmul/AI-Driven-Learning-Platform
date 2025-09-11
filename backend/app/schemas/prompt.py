"""
Prompt Pydantic schemas for API request and response validation.
Defines data structures for prompt and AI response operations.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class PromptBase(BaseModel):
    """Base prompt schema with common fields."""
    prompt: str = Field(..., min_length=10, max_length=2000, description="User's learning prompt")
    category_id: Optional[int] = Field(None, description="Selected category ID")
    sub_category_id: Optional[int] = Field(None, description="Selected subcategory ID")

    @field_validator('prompt')
    @classmethod
    def validate_prompt(cls, v):
        if not v.strip():
            raise ValueError('Prompt cannot be empty')
        if len(v.strip()) < 10:
            raise ValueError('Prompt must be at least 10 characters long')
        return v.strip()


class PromptCreate(PromptBase):
    """Schema for prompt creation."""
    pass


class PromptUpdate(BaseModel):
    """Schema for prompt updates (mainly for admin)."""
    response: Optional[str] = Field(None, description="AI response content")
    ai_model: Optional[str] = Field(None, max_length=50, description="AI model used")
    response_time_ms: Optional[int] = Field(None, description="Response time in milliseconds")


class PromptResponse(PromptBase):
    """Schema for prompt responses."""
    id: int
    user_id: int
    response: Optional[str] = Field(None, description="AI generated response")
    ai_model: str = Field(default="gpt-3.5-turbo", description="AI model used")
    response_time_ms: Optional[int] = Field(None, description="Response time in milliseconds")
    created_at: datetime

    class Config:
        from_attributes = True


class PromptWithRelations(PromptResponse):
    """Schema for prompt responses with related data."""
    user_name: Optional[str] = Field(None, description="User's name")
    user_email: Optional[str] = Field(None, description="User's email")
    category_name: Optional[str] = Field(None, description="Category name")
    sub_category_name: Optional[str] = Field(None, description="SubCategory name")


class PromptListResponse(BaseModel):
    """Schema for paginated prompt list responses."""
    prompts: List[PromptResponse]
    total: int
    page: int
    size: int
    total_pages: int


class PromptHistoryResponse(BaseModel):
    """Schema for user's prompt history."""
    prompts: List[PromptWithRelations]
    total: int
    page: int
    size: int
    total_pages: int


class AIGenerationRequest(BaseModel):
    """Schema for AI generation requests."""
    prompt: str = Field(..., min_length=10, max_length=2000)
    category_context: Optional[str] = Field(None, description="Category context for AI")
    subcategory_context: Optional[str] = Field(None, description="SubCategory context for AI")
    user_context: Optional[str] = Field(None, description="User learning context")


class AIGenerationResponse(BaseModel):
    """Schema for AI generation responses."""
    response: str = Field(..., description="Generated AI response")
    ai_model: str = Field(..., description="AI model that generated the response")
    response_time_ms: int = Field(..., description="Time taken to generate response")
    tokens_used: Optional[int] = Field(None, description="Number of tokens used")

    model_config = {"protected_namespaces": ()}


class PromptSearchRequest(BaseModel):
    """Schema for prompt search requests."""
    query: Optional[str] = Field(None, description="Text search query")
    category_id: Optional[int] = Field(None, description="Filter by category")
    sub_category_id: Optional[int] = Field(None, description="Filter by subcategory")
    user_id: Optional[int] = Field(None, description="Filter by user (admin only)")
    date_from: Optional[datetime] = Field(None, description="Filter from date")
    date_to: Optional[datetime] = Field(None, description="Filter to date")


class PromptStatsResponse(BaseModel):
    """Schema for prompt statistics."""
    total_prompts: int
    prompts_today: int
    prompts_this_week: int
    prompts_this_month: int
    average_response_time_ms: Optional[float]
    most_used_category: Optional[str]
    most_active_user: Optional[str]
    ai_model_usage: dict  # Model name -> count


class BulkPromptResponse(BaseModel):
    """Schema for bulk prompt operations."""
    processed: int
    successful: int
    failed: int
    errors: List[str]
