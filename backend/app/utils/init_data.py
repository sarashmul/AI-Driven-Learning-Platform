"""
Initialize production database with default data.
Creates categories, admin user, and basic setup.
"""
import asyncio
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..core.database import SessionLocal
from ..models.user import User
from ..models.category import Category, SubCategory
from ..utils.security import hash_password

def create_default_categories(db: Session) -> bool:
    """Create default categories and subcategories."""
    try:
        # Check if categories already exist
        existing_categories = db.query(Category).count()
        if existing_categories > 0:
            print("✅ Categories already exist")
            return True
        
        print("🔨 Creating default categories...")
        
        # Technology category
        tech_category = Category(
            name="Technology",
            description="Programming, software development, and tech topics"
        )
        db.add(tech_category)
        db.flush()  # Get the ID
        
        tech_subcategories = [
            SubCategory(name="Python Programming", category_id=tech_category.id),
            SubCategory(name="Web Development", category_id=tech_category.id),
            SubCategory(name="Data Science", category_id=tech_category.id),
            SubCategory(name="Machine Learning", category_id=tech_category.id),
        ]
        
        # Science category
        science_category = Category(
            name="Science",
            description="Natural sciences, physics, chemistry, biology"
        )
        db.add(science_category)
        db.flush()
        
        science_subcategories = [
            SubCategory(name="Physics", category_id=science_category.id),
            SubCategory(name="Chemistry", category_id=science_category.id),
            SubCategory(name="Biology", category_id=science_category.id),
            SubCategory(name="Mathematics", category_id=science_category.id),
        ]
        
        # Language category
        language_category = Category(
            name="Language",
            description="Language learning and linguistics"
        )
        db.add(language_category)
        db.flush()
        
        language_subcategories = [
            SubCategory(name="English", category_id=language_category.id),
            SubCategory(name="Spanish", category_id=language_category.id),
            SubCategory(name="French", category_id=language_category.id),
            SubCategory(name="Hebrew", category_id=language_category.id),
        ]
        
        # Add all subcategories
        for subcat in tech_subcategories + science_subcategories + language_subcategories:
            db.add(subcat)
        
        db.commit()
        print("✅ Default categories created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create categories: {e}")
        db.rollback()
        return False

def create_admin_user(db: Session) -> bool:
    """Create default admin user."""
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.email == "admin@admin.com").first()
        if existing_admin:
            print("✅ Admin user already exists")
            return True
        
        print("👨‍💼 Creating admin user...")
        
        admin_user = User(
            name="Admin User",
            email="admin@admin.com",
            password_hash=hash_password("admin123"),
            is_active=True,
            role="admin"
        )
        
        db.add(admin_user)
        db.commit()
        
        print("✅ Admin user created successfully")
        print("📧 Email: admin@admin.com")
        print("🔑 Password: admin123")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create admin user: {e}")
        db.rollback()
        return False

def initialize_production_data() -> bool:
    """Initialize production database with default data."""
    print("🚀 Initializing production database...")
    
    try:
        db = SessionLocal()
        
        # Create categories
        categories_ok = create_default_categories(db)
        
        # Create admin user
        admin_ok = create_admin_user(db)
        
        db.close()
        
        if categories_ok and admin_ok:
            print("🎉 Production database initialized successfully!")
            return True
        else:
            print("⚠️ Some initialization steps failed")
            return False
            
    except Exception as e:
        print(f"💥 Failed to initialize production database: {e}")
        return False

if __name__ == "__main__":
    # Can be run directly for testing
    initialize_production_data()