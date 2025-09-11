"""
Category API routes for public category and subcategory access.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import traceback

from ..core.database import get_db
from ..models.category import Category, SubCategory
from ..schemas.category import CategoryResponse, SubCategoryResponse

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    """Get all active categories."""
    try:
        categories = db.query(Category).filter(Category.is_active == True).all()
        result = [CategoryResponse.model_validate(cat) for cat in categories]
        return result
    except Exception as e:
        print(f"Error in get_categories: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{category_id}/subcategories", response_model=List[SubCategoryResponse])
async def get_subcategories(
    category_id: int,
    db: Session = Depends(get_db)
):
    """Get all active subcategories for a category."""
    try:
        subcategories = db.query(SubCategory).filter(
            SubCategory.category_id == category_id,
            SubCategory.is_active == True
        ).all()
        result = [SubCategoryResponse.model_validate(subcat) for subcat in subcategories]
        return result
    except Exception as e:
        print(f"Error in get_subcategories: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Simple test route
@router.get("/test")
async def test_route():
    """Simple test route to verify routing works."""
    return {"message": "Categories router is working!", "status": "success"}
