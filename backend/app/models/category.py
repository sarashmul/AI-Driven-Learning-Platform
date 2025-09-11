"""
Category and SubCategory SQLAlchemy models.
Implements hierarchical category structure with soft delete capability.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class Category(Base):
    """
    Main category model with soft delete functionality.
    
    Categories contain multiple subcategories and track creation metadata.
    """
    __tablename__ = "categories"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Category information
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, server_default='true')
    
    # Metadata
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.current_timestamp(), server_default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    creator = relationship("User", back_populates="created_categories")
    subcategories = relationship("SubCategory", back_populates="category", cascade="all, delete-orphan")
    prompts = relationship("Prompt", back_populates="category")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', active={self.is_active})>"
    
    def to_dict(self):
        """Convert category to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class SubCategory(Base):
    """
    Sub-category model with parent category relationship.
    
    SubCategories belong to a parent category and support hierarchical organization.
    """
    __tablename__ = "sub_categories"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # SubCategory information
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Parent relationship
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Status
    is_active = Column(Boolean, default=True, server_default='true')
    
    # Metadata
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.current_timestamp(), server_default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    category = relationship("Category", back_populates="subcategories")
    creator = relationship("User", back_populates="created_subcategories")
    prompts = relationship("Prompt", back_populates="sub_category")
    
    def __repr__(self):
        return f"<SubCategory(id={self.id}, name='{self.name}', category_id={self.category_id})>"
    
    def to_dict(self):
        """Convert subcategory to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category_id": self.category_id,
            "is_active": self.is_active,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
