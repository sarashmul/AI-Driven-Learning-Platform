#!/usr/bin/env python3
"""
Final comprehensive OpenAI test with detailed error info
"""
import openai
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Get API key
api_key = os.getenv('OPENAI_API_KEY')

print("🔍 OpenAI Integration Final Test")
print("=" * 50)
print(f"🔑 API Key present: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"🔑 Key format: {api_key[:8]}...{api_key[-6:]}")
    print(f"🔑 Key length: {len(api_key)}")

print(f"🐍 Python version: {sys.version}")
print(f"📦 OpenAI version: {openai.__version__}")

if not api_key:
    print("❌ No API key found!")
    sys.exit(1)

try:
    print("\n📡 Testing API connection...")
    
    # Initialize client with explicit settings
    client = openai.OpenAI(
        api_key=api_key,
        timeout=30.0
    )
    
    print("✅ Client initialized")
    
    # Test request with verbose error handling
    print("📤 Sending test request to OpenAI...")
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user", 
            "content": "Respond with exactly: SUCCESS"
        }],
        max_tokens=10,
        temperature=0
    )
    
    if response and response.choices:
        result = response.choices[0].message.content.strip()
        print(f"📥 Raw response: {result}")
        
        if "SUCCESS" in result:
            print("🎉 PERFECT! OpenAI API is working!")
            print("✅ Ready for production use")
        else:
            print(f"⚠️  API working but unexpected response: {result}")
    else:
        print("❌ Empty response from API")

except openai.AuthenticationError as e:
    print(f"🔐 Authentication Error: {e}")
    print("💡 Check your API key - it might be invalid or expired")
    
except openai.RateLimitError as e:
    print(f"🚦 Rate Limit Error: {e}")
    print("💡 You've hit the API rate limit")
    
except openai.APIConnectionError as e:
    print(f"🌐 Connection Error: {e}")
    print("💡 Network issue - check internet connection")
    
except openai.APIError as e:
    print(f"🔧 API Error: {e}")
    print("💡 OpenAI service issue")
    
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    print(f"❌ Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
