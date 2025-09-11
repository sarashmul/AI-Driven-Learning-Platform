"""
Prompt API routes for user prompt submissions and history.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..core.auth import get_current_user
from ..models.user import User
from ..models.prompt import Prompt
from ..models.category import Category, SubCategory
from ..schemas.prompt import PromptResponse, PromptCreate, PromptWithRelations
from ..services.ai_service import AIService
from ..core.exceptions import AIServiceException

router = APIRouter()
ai_service = AIService()


@router.get("/my-history", response_model=List[PromptWithRelations])
async def get_my_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's prompt history."""
    try:
        print(f"🔍 DEBUG: Getting history for user {current_user.id}")
        
        # שליפה עם joins לקטגוריות
        prompts_query = db.query(
            Prompt, 
            Category.name.label('category_name'),
            SubCategory.name.label('sub_category_name')
        ).outerjoin(
            Category, Prompt.category_id == Category.id
        ).outerjoin(
            SubCategory, Prompt.sub_category_id == SubCategory.id
        ).filter(
            Prompt.user_id == current_user.id
        ).order_by(Prompt.created_at.desc()).limit(20)
        
        results = prompts_query.all()
        print(f"🔍 DEBUG: Found {len(results)} prompts")
        
        # אם אין prompts, נחזיר רשימה ריקה
        if not results:
            print("🔍 DEBUG: No prompts found, returning empty list")
            return []
        
        # יצירת תגובה עם פרטי הקטגוריות
        result = []
        for prompt, category_name, sub_category_name in results:
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
                "user_name": current_user.name,
                "user_email": current_user.email,
                "category_name": category_name,
                "sub_category_name": sub_category_name
            }
            result.append(PromptWithRelations(**prompt_data))
        
        print(f"🔍 DEBUG: Successfully processed {len(result)} prompts")
        print(f"🔍 DEBUG: First prompt categories: {result[0].category_name if result else 'None'}, {result[0].sub_category_name if result else 'None'}")
        return result
        
    except Exception as e:
        print(f"❌ DEBUG: Error in get_my_history: {e}")
        # במקרה של שגיאה, נחזיר רשימה ריקה
        return []


@router.post("/", response_model=PromptResponse)
async def create_prompt(
    prompt_data: PromptCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new prompt and generate AI response."""
    try:
        print(f"🔍 DEBUG: Received prompt_data: {prompt_data}")
        print(f"🔍 DEBUG: Prompt length: {len(prompt_data.prompt) if prompt_data.prompt else 0}")
        print(f"🔍 DEBUG: Current user: {current_user.id}")
        
        # Get category and subcategory names for context
        category_name = None
        subcategory_name = None
        
        if prompt_data.category_id:
            category = db.query(Category).filter(Category.id == prompt_data.category_id).first()
            if category:
                category_name = category.name
        
        if prompt_data.sub_category_id:
            subcategory = db.query(SubCategory).filter(SubCategory.id == prompt_data.sub_category_id).first()
            if subcategory:
                subcategory_name = subcategory.name
        
        # Generate AI response
        ai_response = ai_service.generate_lesson(
            prompt=prompt_data.prompt,
            category_name=category_name,
            subcategory_name=subcategory_name,
            user_context=f"User: {current_user.name or current_user.email}"
        )
        
        # Create new prompt record
        new_prompt = Prompt(
            user_id=current_user.id,
            category_id=prompt_data.category_id,
            sub_category_id=prompt_data.sub_category_id,
            prompt=prompt_data.prompt,
            response=ai_response["response"],
            ai_model=ai_response["model_used"],
            response_time_ms=ai_response["response_time_ms"]
        )
        
        db.add(new_prompt)
        db.commit()
        db.refresh(new_prompt)
        
        return PromptResponse.model_validate(new_prompt)
        
    except AIServiceException as e:
        raise HTTPException(status_code=503, detail=f"AI service error: {str(e)}")
    except Exception as e:
        print(f"❌ DEBUG: Error in create_prompt: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to process prompt")


@router.get("/{prompt_id}", response_model=PromptResponse)
async def get_prompt(
    prompt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific prompt."""
    prompt = db.query(Prompt).filter(
        Prompt.id == prompt_id,
        Prompt.user_id == current_user.id
    ).first()
    
    if not prompt:
        from ..core.exceptions import PromptNotFoundException
        raise PromptNotFoundException(prompt_id)
    
    return PromptResponse.model_validate(prompt)
