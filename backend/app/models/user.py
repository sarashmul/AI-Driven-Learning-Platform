"""
User SQLAlchemy model with role-based access control.
Implements the users table schema with authentication features.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class User(Base):
    """
    User model with role-based access control.
    
    Supports 'user' and 'admin' roles with authentication tracking.
    """
    __tablename__ = "users"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # User information
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    
    # Authentication
    password_hash = Column(String(255), nullable=False)
    role = Column(
        String(10), 
        nullable=False, 
        default='user',
        server_default='user'
    )
    
    # Status and tracking
    is_active = Column(Boolean, default=True, server_default='true')
    last_login = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.current_timestamp(), server_default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Add check constraint for role
    __table_args__ = (
        CheckConstraint(
            "role IN ('user', 'admin')",
            name='check_user_role'
        ),
    )
    
    # Relationships
    created_categories = relationship("Category", back_populates="creator")
    created_subcategories = relationship("SubCategory", back_populates="creator")
    prompts = relationship("Prompt", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
    
    def to_dict(self):
        """Convert user to dictionary (excluding sensitive data)."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "is_active": self.is_active,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
