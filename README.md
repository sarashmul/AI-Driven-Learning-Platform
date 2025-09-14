# 🚀 AI-Driven Learning Platform

> A modern, full-stack learning platform powered by AI that generates personalized educational content based on user prompts and categories.

## 🌟 Live Demo

**🔗 [Visit the Live Application](https://ai-driven-learning-platform-frontend.onrender.com/)**

Experience the platform live in the cloud! Create an account and start generating AI-powered lessons instantly.

---

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [API Documentation](#-api-documentation)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🎯 Core Features
- **AI-Powered Learning**: Generate personalized educational content using OpenAI's GPT models
- **Smart Categories**: Organized learning topics with hierarchical category system
- **User Authentication**: Secure JWT-based authentication with role-based access
- **Learning History**: Track and revisit all your generated lessons
- **Admin Dashboard**: Comprehensive management panel for users, content, and analytics
- **Responsive Design**: Beautiful Material-UI interface that works on all devices

### 🔐 Authentication & Security
- JWT token-based authentication
- Role-based access control (User/Admin)
- Secure password hashing with bcrypt
- Protected routes and API endpoints
- Session management with auto-refresh

### 🤖 AI Integration
- **OpenAI GPT Integration**: Leverages GPT-3.5-turbo for content generation
- **Context-Aware Responses**: AI considers category and user preferences
- **Response Optimization**: Formatted, educational content delivery
- **Performance Tracking**: Monitor AI response times and quality

### 📊 Admin Features
- User management and analytics
- Content moderation and oversight
- System health monitoring
- Category and subcategory management
- Learning statistics and insights

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.13+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with python-jose
- **AI Service**: OpenAI GPT-3.5-turbo API
- **Migrations**: Alembic for database versioning
- **Security**: Passlib for password hashing
- **Validation**: Pydantic for data validation

### Frontend
- **Framework**: React 19+ with Vite
- **UI Library**: Material-UI (MUI) v7
- **Routing**: React Router DOM v7
- **HTTP Client**: Axios for API communication
- **State Management**: React Context + Hooks
- **Styling**: Custom green-blue gradient theme

### Infrastructure
- **Deployment**: Render.com (Cloud hosting)
- **Database**: PostgreSQL (Production)
- **Environment**: Docker-ready containers
- **Development**: Hot reload for both frontend and backend

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React SPA     │    │   FastAPI       │    │   PostgreSQL    │
│   (Frontend)    │◄──►│   (Backend)     │◄──►│   (Database)    │
│                 │    │                 │    │                 │
│ • Material-UI   │    │ • JWT Auth      │    │ • User Data     │
│ • Route Guards  │    │ • AI Service    │    │ • Categories    │
│ • State Mgmt    │    │ • API Endpoints │    │ • Learning Logs │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   OpenAI API    │
                       │   (AI Service)  │
                       │                 │
                       │ • GPT-3.5-turbo │
                       │ • Lesson Gen    │
                       │ • Content AI    │
                       └─────────────────┘
```

### Data Flow
1. **User Authentication**: Login/Register → JWT Token → Protected Routes
2. **Learning Flow**: Category Selection → Prompt Input → AI Processing → Response Display → History Save
3. **Admin Flow**: Admin Dashboard → User Management → Content Oversight → Analytics

---

## 🚀 Quick Start

### Option 1: Use the Live Application
Simply visit **[https://ai-driven-learning-platform-frontend.onrender.com/](https://ai-driven-learning-platform-frontend.onrender.com/)** and start learning immediately!

### Option 2: Run Locally
Follow the [Installation](#-installation) guide below to set up the full development environment.

---

## 💻 Installation

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.13+
- **PostgreSQL** 14+ (or use SQLite for development)
- **Git**

### 1. Clone the Repository
```bash
git clone https://github.com/sarashmul/AI-Driven-Learning-Platform.git
cd AI-Driven-Learning-Platform
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration (see Environment Variables section)

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

The backend will be available at `http://localhost:8001`

### 3. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 4. Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/ai_learning_platform
# For development, you can use SQLite:
# DATABASE_URL=sqlite:///./learning_platform.db

# JWT Security
SECRET_KEY=your-super-secret-jwt-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Application Settings
DEBUG=true
APP_NAME=AI-Driven Learning Platform
ALLOWED_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Pagination
DEFAULT_PAGE_SIZE=10
MAX_PAGE_SIZE=100
```

### 5. Get Your OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add it to your `.env` file
4. Ensure your OpenAI account has sufficient credits

---

## 📚 API Documentation

Once the backend is running, explore the interactive API documentation:

- **Swagger UI**: [http://localhost:8001/docs](http://localhost:8001/docs)
- **ReDoc**: [http://localhost:8001/redoc](http://localhost:8001/redoc)
- **Health Check**: [http://localhost:8001/health](http://localhost:8001/health)

### Key API Endpoints

#### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user profile

#### Learning
- `GET /api/categories/` - List all categories
- `GET /api/categories/{id}/subcategories` - Get subcategories
- `POST /api/prompts/` - Generate AI lesson
- `GET /api/prompts/my-history` - Get user's learning history

#### Admin (Admin users only)
- `GET /api/admin/users` - Manage users
- `GET /api/admin/prompts` - View all prompts
- `POST /api/admin/categories` - Create categories

---

## 🖼️ Screenshots

### 🎯 Learning Dashboard
The main interface where users select categories and generate AI-powered lessons.

### 📚 Learning History
Track and revisit all your generated educational content with search and filtering.

### 👨‍💼 Admin Panel
Comprehensive management dashboard for administrators to oversee users and content.

### 📱 Mobile Responsive
Beautiful Material-UI design that works perfectly on all devices.

---

## 🧪 Testing

### Backend Testing
```bash
cd backend
python test_setup.py  # Test configuration and services
python test_openai.py  # Test AI integration
```

### Frontend Testing
```bash
cd frontend
npm run lint          # Run ESLint
npm run build         # Test production build
```

---

## 🚀 Deployment

The application is configured for easy deployment on various platforms:

### Render.com (Recommended)
- Frontend: Automatically deploys from main branch
- Backend: Uses Docker container with PostgreSQL addon
- Environment variables configured in Render dashboard

### Docker
```bash
# Backend
cd backend
docker build -t ai-learning-backend .
docker run -p 8001:8001 ai-learning-backend

# Frontend
cd frontend
npm run build
# Serve the dist folder with any static file server
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow the existing code style
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/sarashmul/AI-Driven-Learning-Platform/issues)
- **Documentation**: Check out the `/docs` folder for detailed guides
- **API Docs**: Visit the live Swagger documentation when running locally

---

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT API for AI-powered content generation
- **Material-UI** for the beautiful React components
- **FastAPI** for the excellent Python web framework
- **Render.com** for reliable cloud hosting

---

<div align="center">

**Built with ❤️ using FastAPI, React, and OpenAI**

[🌟 Star this repository](https://github.com/sarashmul/AI-Driven-Learning-Platform) if you find it helpful!

</div>