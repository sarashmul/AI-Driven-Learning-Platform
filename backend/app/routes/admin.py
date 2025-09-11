"""
Admin API routes for administrative functions.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..core.auth import get_current_admin_user
from ..models.user import User
from ..models.prompt import Prompt
from ..models.category import Category, SubCategory
from ..schemas.user import UserResponse
from ..schemas.prompt import PromptWithRelations

router = APIRouter()


@router.get("/stats")
async def get_admin_stats(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get administrative statistics."""
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    admin_users = db.query(User).filter(User.role == 'admin').count()
    total_prompts = db.query(Prompt).count()
    total_categories = db.query(Category).count()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "admin_users": admin_users,
        "total_prompts": total_prompts,
        "total_categories": total_categories,
        "admin_user": current_admin.email
    }


@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all users for admin panel."""
    users = db.query(User).order_by(User.created_at.desc()).limit(50).all()
    return users


@router.get("/prompts", response_model=List[PromptWithRelations])
async def get_all_prompts(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all prompts for admin panel."""
    prompts_query = db.query(
        Prompt, 
        User.name.label('user_name'),
        User.email.label('user_email'),
        Category.name.label('category_name'),
        SubCategory.name.label('sub_category_name')
    ).join(
        User, Prompt.user_id == User.id
    ).outerjoin(
        Category, Prompt.category_id == Category.id
    ).outerjoin(
        SubCategory, Prompt.sub_category_id == SubCategory.id
    ).order_by(Prompt.created_at.desc()).limit(50)
    
    results = prompts_query.all()
    
    # יצירת תגובה עם פרטי המשתמשים והקטגוריות
    result = []
    for prompt, user_name, user_email, category_name, sub_category_name in results:
        prompt_data = {
            "id": prompt.id,
            "user_id": prompt.user_id,
            "prompt": prompt.prompt,
            "category_id": prompt.category_id,
            "sub_category_id": prompt.sub_category_id,
            "response": prompt.response,
            "ai_model": prompt.ai_model,
            "response_time_ms": prompt.response_time_ms,
            "created_at": prompt.created_at,
            "user_name": user_name,
            "user_email": user_email,
            "category_name": category_name,
            "sub_category_name": sub_category_name
        }
        result.append(PromptWithRelations(**prompt_data))
    
    return result
