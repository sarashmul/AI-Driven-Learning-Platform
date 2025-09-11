#!/bin/bash

# AI-Driven Learning Platform - Production Deployment Script
# This script prepares the application for production deployment

echo "🚀 Preparing AI-Driven Learning Platform for Production..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "📝 Please copy .env.example to .env and configure your environment variables:"
    echo "   cp .env.example .env"
    echo "   nano .env"
    exit 1
fi

# Check required environment variables
echo "🔍 Checking environment variables..."

required_vars=("DATABASE_URL" "SECRET_KEY")
missing_vars=()

for var in "${required_vars[@]}"; do
    if ! grep -q "^$var=" .env || grep -q "^$var=$" .env || grep -q "^$var=.*CHANGE.*" .env; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -gt 0 ]; then
    echo "❌ Missing or incomplete environment variables:"
    for var in "${missing_vars[@]}"; do
        echo "   - $var"
    done
    echo "📝 Please configure these variables in your .env file"
    exit 1
fi

# Check if AI API key is configured
if ! grep -q "^OPENAI_API_KEY=" .env && ! grep -q "^GEMINI_API_KEY=" .env; then
    echo "⚠️  Warning: No AI API key configured (OPENAI_API_KEY or GEMINI_API_KEY)"
    echo "   The application will not be able to generate lessons without an AI API key"
fi

echo "✅ Environment check passed!"

# Build and start production services
echo "🐳 Building and starting production services..."
docker-compose -f docker-compose.prod.yml up --build -d

echo "🎉 Production deployment complete!"
echo "📊 Access your application at: http://localhost:8000"
echo "📚 API documentation at: http://localhost:8000/docs"
