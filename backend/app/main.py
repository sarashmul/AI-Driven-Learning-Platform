"""
Main FastAPI application entry point.
Configures the application, middleware, routes, and startup/shutdown events.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import uvicorn

from .core.config import settings
from .core.database import check_db_connection, create_all_tables
from .core.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
    CategoryNotFoundException,
    SubCategoryNotFoundException,
    PromptNotFoundException,
    AIServiceException,
    DatabaseException,
    ValidationException,
    PermissionDeniedException
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting AI-Driven Learning Platform...")
    
    # Check database connection
    if check_db_connection():
        logger.info("Database connection successful")
        
        # Create tables if they don't exist
        try:
            create_all_tables()
            logger.info("Database tables ready")
            
            # Initialize production data if needed
            try:
                from .utils.init_data import initialize_production_data
                if initialize_production_data():
                    logger.info("Production data initialized")
                else:
                    logger.warning("Some production data initialization failed")
            except Exception as e:
                logger.error(f"Failed to initialize production data: {e}")
                
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
    else:
        logger.error("Database connection failed!")
    
    # Initialize AI service
    try:
        from .services.ai_service import AIService
        ai_service = AIService()
        if ai_service.client:
            logger.info("AI service initialized successfully")
        else:
            logger.warning("AI service not configured - missing API key")
    except Exception as e:
        logger.error(f"Failed to initialize AI service: {e}")
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI-Driven Learning Platform...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="A full-stack learning platform with AI-powered lesson generation",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,  # Changed to False when using "*"
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Manual CORS handler as backup
@app.middleware("http")
async def cors_handler(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# Add preflight OPTIONS handler
@app.options("/{path:path}")
async def options_handler(path: str):
    return {"message": "OK"}


# Global exception handlers
@app.exception_handler(UserAlreadyExistsException)
async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "user_already_exists"}
    )


@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "user_not_found"}
    )


@app.exception_handler(InvalidCredentialsException)
async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "invalid_credentials"}
    )


@app.exception_handler(CategoryNotFoundException)
async def category_not_found_handler(request: Request, exc: CategoryNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "category_not_found"}
    )


@app.exception_handler(SubCategoryNotFoundException)
async def subcategory_not_found_handler(request: Request, exc: SubCategoryNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "subcategory_not_found"}
    )


@app.exception_handler(PromptNotFoundException)
async def prompt_not_found_handler(request: Request, exc: PromptNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "prompt_not_found"}
    )


# @app.exception_handler(AIServiceException)
# async def ai_service_handler(request: Request, exc: AIServiceException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.detail, "type": "ai_service_error"}
#     )


@app.exception_handler(DatabaseException)
async def database_handler(request: Request, exc: DatabaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "database_error"}
    )


@app.exception_handler(ValidationException)
async def validation_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "validation_error"}
    )


@app.exception_handler(PermissionDeniedException)
async def permission_denied_handler(request: Request, exc: PermissionDeniedException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "permission_denied"}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": "internal_error"}
    )


# Health check endpoints
@app.get("/")
async def root():
    """Root endpoint with basic application info."""
    return {
        "message": "AI-Driven Learning Platform API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint."""
    # from .services.ai_service import ai_service
    
    health_status = {
        "status": "healthy",
        "database": check_db_connection(),
        "ai_service": False,  # ai_service.health_check(),
        "timestamp": "2024-12-19T10:00:00Z"
    }
    
    # Determine overall status
    if not health_status["database"]:
        health_status["status"] = "unhealthy"
    elif not health_status["ai_service"]:
        health_status["status"] = "degraded"
    
    status_code = 200 if health_status["status"] != "unhealthy" else 503
    
    return JSONResponse(
        status_code=status_code,
        content=health_status
    )


# Import and include routers
from .routes import auth, categories, prompts, admin

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(prompts.router, prefix="/api/prompts", tags=["Prompts"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )
