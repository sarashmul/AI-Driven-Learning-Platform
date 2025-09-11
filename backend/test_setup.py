"""
Simple test script to verify backend setup and database connection.
"""
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from app.core.config import settings
from app.core.database import check_db_connection, create_all_tables
from app.services.ai_service import ai_service

def test_configuration():
    """Test application configuration."""
    print("🔧 Testing Application Configuration...")
    print(f"   App Name: {settings.app_name}")
    print(f"   Debug Mode: {settings.debug}")
    print(f"   Database URL: {settings.database_url}")
    print(f"   OpenAI API Key: {'✅ Set' if settings.openai_api_key else '❌ Not Set'}")
    print()

def test_database():
    """Test database connection."""
    print("🗄️ Testing Database Connection...")
    if check_db_connection():
        print("   ✅ Database connection successful")
        try:
            create_all_tables()
            print("   ✅ Database tables created/verified")
        except Exception as e:
            print(f"   ❌ Failed to create tables: {e}")
    else:
        print("   ❌ Database connection failed")
    print()

def test_ai_service():
    """Test AI service."""
    print("🤖 Testing AI Service...")
    model_info = ai_service.get_model_info()
    print(f"   Model: {model_info['model_name']}")
    print(f"   Provider: {model_info['provider']}")
    print(f"   Available: {'✅' if model_info['available'] else '❌'}")
    print(f"   API Configured: {'✅' if model_info['api_configured'] else '❌'}")
    
    if ai_service.health_check():
        print("   ✅ AI service health check passed")
    else:
        print("   ❌ AI service health check failed")
    print()

if __name__ == "__main__":
    print("🚀 AI-Driven Learning Platform - Backend Test")
    print("=" * 50)
    
    test_configuration()
    test_database()
    test_ai_service()
    
    print("✅ Backend setup test completed!")
    print("\nNext steps:")
    print("1. Set up PostgreSQL database")
    print("2. Configure OPENAI_API_KEY in .env file")
    print("3. Run: uvicorn app.main:app --reload")
