# AI-Driven Learning Platform - Backend

A FastAPI-based backend for the AI-Driven Learning Platform with JWT authentication, PostgreSQL database, and Google Gemini AI integration.

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- PostgreSQL database
- Google Gemini API key

### Installation

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Activate virtual environment:**
   ```bash
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env file with your configuration:
   # - DATABASE_URL
   # - GEMINI_API_KEY
   # - SECRET_KEY
   ```

5. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start the development server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📋 API Documentation

Once the server is running, visit:
- **Interactive API Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── core/           # Core configuration and utilities
│   │   ├── config.py   # Environment settings
│   │   ├── database.py # Database connection
│   │   ├── auth.py     # JWT authentication
│   │   └── exceptions.py # Custom exceptions
│   ├── models/         # SQLAlchemy database models
│   │   ├── user.py     # User model
│   │   ├── category.py # Category & SubCategory models
│   │   └── prompt.py   # Prompt model
│   ├── schemas/        # Pydantic schemas for API validation
│   │   ├── auth.py     # Authentication schemas
│   │   ├── user.py     # User schemas
│   │   ├── category.py # Category schemas
│   │   └── prompt.py   # Prompt schemas
│   ├── routes/         # FastAPI route handlers
│   │   ├── auth.py     # Authentication endpoints
│   │   ├── categories.py # Category endpoints
│   │   ├── prompts.py  # Prompt endpoints
│   │   └── admin.py    # Admin endpoints
│   ├── services/       # Business logic services
│   │   ├── auth_service.py # Authentication logic
│   │   ├── ai_service.py   # AI integration
│   │   └── ...
│   ├── utils/          # Utility functions
│   │   ├── security.py # Password hashing
│   │   └── validators.py # Input validation
│   └── main.py         # FastAPI application entry point
├── alembic/            # Database migration files
├── requirements.txt    # Python dependencies
├── .env.example       # Environment configuration template
└── test_setup.py      # Backend setup verification script
```

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info
- `PUT /api/auth/profile` - Update user profile

### Categories (Public)
- `GET /api/categories` - List all categories
- `GET /api/categories/{id}/subcategories` - Get subcategories

### Prompts (Protected)
- `POST /api/prompts` - Submit learning prompt
- `GET /api/prompts/my-history` - Get user's prompt history
- `GET /api/prompts/{id}` - Get specific prompt

### Admin (Admin Only)
- `GET /api/admin/stats` - System statistics
- `GET /api/admin/users` - User management
- `POST /api/admin/categories` - Category management
- `GET /api/admin/prompts` - All prompts overview

## 🗄️ Database Schema

The application uses the following database tables:

### Users Table
- User authentication and profile information
- Role-based access control (user/admin)
- Activity tracking and timestamps

### Categories & SubCategories
- Hierarchical category structure
- Soft delete functionality
- Creation metadata tracking

### Prompts Table
- User learning prompts and AI responses
- Performance metrics (response time)
- Category associations

## 🤖 AI Integration

The backend integrates with Google Gemini AI for:
- Learning lesson generation
- Context-aware responses
- Prompt enhancement and optimization

### AI Features:
- Enhanced prompts with category context
- Response time tracking
- Content validation and filtering
- Health monitoring

## 🔐 Security Features

- **JWT Authentication** with configurable expiration
- **Password hashing** using bcrypt
- **Role-based access control** (user/admin)
- **Input validation** and sanitization
- **CORS configuration** for secure API calls

## 🧪 Testing

Run the backend setup test:
```bash
python test_setup.py
```

This will verify:
- ✅ Configuration loading
- ✅ Database connectivity
- ✅ AI service availability

## 📦 Dependencies

### Core Dependencies
- **FastAPI** - Modern web framework
- **SQLAlchemy** - Database ORM
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **psycopg2** - PostgreSQL adapter

### Authentication & Security
- **python-jose** - JWT handling
- **passlib** - Password hashing
- **python-multipart** - Form data handling

### AI Integration
- **google-generativeai** - Gemini AI client

## 🔧 Configuration

Key environment variables:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# JWT Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Service
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-pro

# Application
DEBUG=False
ALLOWED_ORIGINS=["http://localhost:3000"]
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Verify PostgreSQL is running
   - Check DATABASE_URL in .env file
   - Ensure database exists and credentials are correct

2. **AI Service Not Available**
   - Set GEMINI_API_KEY in .env file
   - Verify API key is valid and has quota

3. **Import Errors**
   - Ensure virtual environment is activated
   - Check all dependencies are installed: `pip install -r requirements.txt`

## 📄 License

This project is part of the AI-Driven Learning Platform educational project.
