"""
Category Pydantic schemas for API request and response validation.
Defines data structures for category and subcategory operations.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class CategoryBase(BaseModel):
    """Base category schema with common fields."""
    name: str = Field(..., min_length=2, max_length=100, description="Category name")
    description: Optional[str] = Field(None, max_length=500, description="Category description")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Category name cannot be empty')
        # Allow letters, numbers, spaces, and hyphens
        import re
        if not re.match(r"^[a-zA-Z0-9\s\-]+$", v.strip()):
            raise ValueError('Category name can only contain letters, numbers, spaces, and hyphens')
        return v.strip()


class CategoryCreate(CategoryBase):
    """Schema for category creation."""
    pass


class CategoryUpdate(BaseModel):
    """Schema for category updates."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = Field(None, description="Whether category is active")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Category name cannot be empty')
            import re
            if not re.match(r"^[a-zA-Z0-9\s\-]+$", v.strip()):
                raise ValueError('Category name can only contain letters, numbers, spaces, and hyphens')
            return v.strip()
        return v


class SubCategoryBase(BaseModel):
    """Base subcategory schema with common fields."""
    name: str = Field(..., min_length=2, max_length=100, description="SubCategory name")
    description: Optional[str] = Field(None, max_length=500, description="SubCategory description")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('SubCategory name cannot be empty')
        import re
        if not re.match(r"^[a-zA-Z0-9\s\-]+$", v.strip()):
            raise ValueError('SubCategory name can only contain letters, numbers, spaces, and hyphens')
        return v.strip()


class SubCategoryCreate(SubCategoryBase):
    """Schema for subcategory creation."""
    category_id: int = Field(..., description="Parent category ID")


class SubCategoryUpdate(BaseModel):
    """Schema for subcategory updates."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = Field(None, description="Whether subcategory is active")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('SubCategory name cannot be empty')
            import re
            if not re.match(r"^[a-zA-Z0-9\s\-]+$", v.strip()):
                raise ValueError('SubCategory name can only contain letters, numbers, spaces, and hyphens')
            return v.strip()
        return v


class SubCategoryResponse(SubCategoryBase):
    """Schema for subcategory responses."""
    id: int
    category_id: int
    is_active: bool
    created_by: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CategoryResponse(CategoryBase):
    """Schema for category responses."""
    id: int
    is_active: bool
    created_by: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CategoryWithSubCategories(CategoryResponse):
    """Schema for category responses including subcategories."""
    subcategories: List[SubCategoryResponse] = Field(default_factory=list)


class CategoryListResponse(BaseModel):
    """Schema for paginated category list responses."""
    categories: List[CategoryResponse]
    total: int
    page: int
    size: int
    total_pages: int


class SubCategoryListResponse(BaseModel):
    """Schema for paginated subcategory list responses."""
    subcategories: List[SubCategoryResponse]
    total: int
    page: int
    size: int
    total_pages: int


class CategoryStatsResponse(BaseModel):
    """Schema for category statistics."""
    total_categories: int
    active_categories: int
    total_subcategories: int
    active_subcategories: int
    categories_with_prompts: int
    most_popular_category: Optional[str]
