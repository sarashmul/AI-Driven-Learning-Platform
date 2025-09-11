#!/usr/bin/env python3
"""
Direct OpenAI API test
"""
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Get API key
api_key = os.getenv('OPENAI_API_KEY')
print(f"🔑 API Key: {api_key[:10]}...{api_key[-4:] if api_key and len(api_key) > 10 else 'None'}")

if not api_key:
    print("❌ No API key found")
    exit(1)

try:
    # Initialize client
    client = openai.OpenAI(api_key=api_key)
    print("✅ OpenAI client initialized")
    
    # Test simple request
    print("📤 Sending test request...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'OpenAI API is working!'"}],
        max_tokens=20
    )
    
    print("📥 Response received!")
    print(f"✅ OpenAI Response: {response.choices[0].message.content}")
    print("🎉 OpenAI API is working perfectly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"❌ Error type: {type(e).__name__}")
