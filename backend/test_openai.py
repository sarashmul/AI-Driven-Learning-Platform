"""
Test script to verify OpenAI API integration
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.services.ai_service import ai_service

def test_openai_connection():
    """Test OpenAI API connection and configuration"""
    print("🔍 Testing OpenAI API Integration...")
    print(f"API Key configured: {'Yes' if settings.openai_api_key else 'No'}")
    print(f"Model: {settings.openai_model}")
    
    if not settings.openai_api_key or settings.openai_api_key == "sk-your-actual-openai-api-key-here":
        print("❌ OpenAI API key not configured properly")
        print("📝 Instructions:")
        print("1. Go to: https://platform.openai.com/api-keys")
        print("2. Create a new API key")
        print("3. Replace 'sk-your-actual-openai-api-key-here' in the .env file")
        print("4. Make sure your OpenAI account has credits")
        return False
    
    try:
        # Test AI service health check
        health_status = ai_service.health_check()
        print(f"AI Service Health: {'✅ Healthy' if health_status else '❌ Not healthy'}")
        
        if health_status:
            print("🎉 OpenAI integration is working!")
            return True
        else:
            print("❌ OpenAI service is not responding properly")
            return False
            
    except Exception as e:
        print(f"❌ Error testing OpenAI: {e}")
        return False

if __name__ == "__main__":
    test_openai_connection()
