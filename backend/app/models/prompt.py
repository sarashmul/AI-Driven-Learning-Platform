"""
Prompt SQLAlchemy model with AI response tracking.
Stores user prompts, AI responses, and performance metrics.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class Prompt(Base):
    """
    Prompt model for storing user prompts and AI responses.
    
    Tracks user learning interactions with categories, subcategories,
    AI responses, and performance metrics.
    """
    __tablename__ = "prompts"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # User relationship
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Category relationships (optional)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    sub_category_id = Column(Integer, ForeignKey("sub_categories.id"), nullable=True)
    
    # Prompt and response content
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    
    # AI model information
    ai_model = Column(String(50), default="gemini-pro", server_default="gemini-pro")
    
    # Performance tracking
    response_time_ms = Column(Integer, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, default=func.current_timestamp(), server_default=func.current_timestamp(), index=True)
    
    # Relationships
    user = relationship("User", back_populates="prompts")
    category = relationship("Category", back_populates="prompts")
    sub_category = relationship("SubCategory", back_populates="prompts")
    
    def __repr__(self):
        return f"<Prompt(id={self.id}, user_id={self.user_id}, category_id={self.category_id})>"
    
    def to_dict(self):
        """Convert prompt to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "sub_category_id": self.sub_category_id,
            "prompt": self.prompt,
            "response": self.response,
            "ai_model": self.ai_model,
            "response_time_ms": self.response_time_ms,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    def to_dict_with_relations(self):
        """Convert prompt to dictionary including related data."""
        data = self.to_dict()
        
        # Add category information if available
        if self.category:
            data["category_name"] = self.category.name
        
        # Add subcategory information if available
        if self.sub_category:
            data["sub_category_name"] = self.sub_category.name
        
        # Add user information
        if self.user:
            data["user_name"] = self.user.name
            data["user_email"] = self.user.email
        
        return data
