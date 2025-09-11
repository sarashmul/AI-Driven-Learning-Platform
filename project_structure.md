# AI-Driven Learning Platform - Project Structure & Architecture

## 📁 Directory Structure
```
ai-learning-platform/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py          # Environment variables & settings
│   │   │   ├── database.py        # Database connection & session
│   │   │   ├── auth.py            # JWT utilities
│   │   │   └── exceptions.py      # Custom exceptions
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py           # User SQLAlchemy model
│   │   │   ├── category.py       # Category & SubCategory models
│   │   │   └── prompt.py         # Prompt model
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py           # User Pydantic schemas
│   │   │   ├── category.py       # Category schemas
│   │   │   ├── prompt.py         # Prompt schemas
│   │   │   └── auth.py           # Authentication schemas
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py           # Authentication endpoints
│   │   │   ├── categories.py     # Category endpoints
│   │   │   ├── prompts.py        # Prompt endpoints
│   │   │   └── admin.py          # Admin endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py   # Authentication business logic
│   │   │   ├── ai_service.py     # OpenAI API integration
│   │   │   ├── user_service.py   # User operations
│   │   │   ├── category_service.py # Category operations
│   │   │   └── prompt_service.py # Prompt operations
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── security.py       # Password hashing utilities
│   │       └── validators.py     # Input validation utilities
│   ├── alembic/
│   │   ├── versions/             # Database migration files
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── docker-compose.yml        # PostgreSQL & Redis setup
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Layout.jsx           # Main app layout with AppBar
│   │   │   │   ├── ProtectedRoute.jsx   # Route protection wrapper
│   │   │   │   ├── AdminRoute.jsx       # Admin-only route wrapper
│   │   │   │   ├── LoadingSpinner.jsx   # Loading component
│   │   │   │   └── ErrorBoundary.jsx    # Error handling component
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.jsx        # Login form component
│   │   │   │   ├── RegisterForm.jsx     # Registration form
│   │   │   │   └── ProfileForm.jsx      # User profile editing
│   │   │   ├── user/
│   │   │   │   ├── CategorySelector.jsx # Category & subcategory selection
│   │   │   │   ├── PromptForm.jsx       # Prompt input form
│   │   │   │   ├── ResponseDisplay.jsx  # AI response display
│   │   │   │   ├── HistoryList.jsx      # User's prompt history
│   │   │   │   └── HistoryItem.jsx      # Single history item
│   │   │   └── admin/
│   │   │       ├── Dashboard.jsx        # Admin main dashboard
│   │   │       ├── StatsCards.jsx       # Statistics overview cards
│   │   │       ├── UsersTable.jsx       # Users management table
│   │   │       ├── UserDetails.jsx      # Individual user details
│   │   │       ├── CategoriesManager.jsx # Categories CRUD interface
│   │   │       ├── CategoryForm.jsx     # Category add/edit form
│   │   │       ├── PromptsTable.jsx     # All prompts table
│   │   │       └── Pagination.jsx       # Reusable pagination component
│   │   ├── pages/
│   │   │   ├── HomePage.jsx            # Landing page
│   │   │   ├── LoginPage.jsx           # Login page
│   │   │   ├── RegisterPage.jsx        # Registration page
│   │   │   ├── LearningPage.jsx        # Main learning interface
│   │   │   ├── HistoryPage.jsx         # User history page
│   │   │   ├── ProfilePage.jsx         # User profile page
│   │   │   └── AdminPage.jsx           # Admin dashboard page
│   │   ├── services/
│   │   │   ├── api.js                  # Axios configuration & interceptors
│   │   │   ├── authService.js          # Authentication API calls
│   │   │   ├── categoryService.js      # Category API calls
│   │   │   ├── promptService.js        # Prompt API calls
│   │   │   └── adminService.js         # Admin API calls
│   │   ├── hooks/
│   │   │   ├── useAuth.js              # Authentication state management
│   │   │   ├── useCategories.js        # Categories state management
│   │   │   ├── usePagination.js        # Pagination logic
│   │   │   └── useLocalStorage.js      # Local storage utilities
│   │   ├── context/
│   │   │   ├── AuthContext.jsx         # Global auth state
│   │   │   └── ThemeContext.jsx        # Theme customization
│   │   ├── theme/
│   │   │   └── muiTheme.js            # Material-UI theme configuration
│   │   ├── utils/
│   │   │   ├── constants.js           # App constants
│   │   │   ├── formatters.js          # Data formatting utilities
│   │   │   └── validators.js          # Form validation utilities
│   │   ├── App.jsx                    # Main App component
│   │   ├── main.jsx                   # Vite entry point
│   │   └── index.css                  # Global styles
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
├── .gitignore
├── README.md                          # Main project documentation
└── PROJECT_STRUCTURE.md              # This file
```

## 🗄️ Database Schema
```sql
-- Users table with role-based access
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(10) DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories table with soft delete
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sub-categories with parent relationship
CREATE TABLE sub_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Prompts with AI response tracking
CREATE TABLE prompts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id),
    sub_category_id INTEGER REFERENCES sub_categories(id),
    prompt TEXT NOT NULL,
    response TEXT,
    ai_model VARCHAR(50) DEFAULT 'gpt-3.5-turbo',
    response_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_prompts_user_id ON prompts(user_id);
CREATE INDEX idx_prompts_created_at ON prompts(created_at);
CREATE INDEX idx_subcategories_category_id ON sub_categories(category_id);
```

## 🔗 API Endpoints Map
```
Authentication Endpoints:
├── POST   /api/auth/register          # User registration
├── POST   /api/auth/login             # User login (returns JWT)
├── POST   /api/auth/logout            # User logout
├── GET    /api/auth/me                # Get current user info
└── PUT    /api/auth/profile           # Update user profile

Category Endpoints (Public):
├── GET    /api/categories             # List all active categories
└── GET    /api/categories/{id}/subcategories # Get subcategories

Prompt Endpoints (Protected):
├── POST   /api/prompts                # Create prompt + AI generation
├── GET    /api/prompts/my-history     # Get user's prompt history
└── GET    /api/prompts/{id}           # Get specific prompt details

Admin Category Management:
├── POST   /api/admin/categories       # Create new category
├── PUT    /api/admin/categories/{id}  # Update category
├── DELETE /api/admin/categories/{id}  # Soft delete category
├── POST   /api/admin/categories/{id}/subcategories # Create subcategory
├── PUT    /api/admin/subcategories/{id} # Update subcategory
└── DELETE /api/admin/subcategories/{id} # Delete subcategory

Admin Dashboard Endpoints:
├── GET    /api/admin/stats            # System statistics
├── GET    /api/admin/users            # List all users (paginated)
├── GET    /api/admin/users/{id}       # Get user details
├── GET    /api/admin/users/{id}/prompts # Get user's all prompts
└── GET    /api/admin/prompts          # List all prompts (paginated)
```

## 🎨 Material-UI Theme Configuration
```javascript
// Color palette: Modern Green-Blue


## 🔄 Data Flow Architecture
```
User Journey - Learning Flow:
User Login → Select Category → Select Sub-Category → Enter Prompt 
→ AI Processing → Save to Database → Display Response → Add to History

Admin Journey - Management Flow:
Admin Login → Dashboard Overview → Manage Users/Categories/Prompts 
→ CRUD Operations → Real-time Updates → Analytics

Authentication Flow:
Registration/Login → JWT Token → Store in Context → API Authorization 
→ Route Protection → Auto-refresh → Logout
```

## 🚀 Key Implementation Notes

### Backend Services:
- **ai_service.py**: OpenAI API integration with error handling and response formatting
- **auth_service.py**: JWT token management, password hashing, user verification
- **category_service.py**: CRUD operations for categories with validation
- **prompt_service.py**: Prompt processing, AI response handling, history management

### Frontend Hooks:
- **useAuth**: Global authentication state, login/logout, token refresh
- **useCategories**: Category/subcategory loading and caching
- **usePagination**: Reusable pagination logic for admin tables

### Security Features:
- Password hashing with bcrypt
- JWT token expiration and refresh
- Protected routes with role-based access
- Input validation and sanitization
- CORS configuration for secure API calls

### Performance Optimizations:
- Database indexing for frequent queries
- API response caching for categories
- Lazy loading for admin dashboard tables
- Optimized AI API calls with timeout handling