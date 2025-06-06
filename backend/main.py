"""
Main FastAPI application entry point for AI-powered e-commerce platform.

This module serves as the central application factory and configuration point for the FastAPI backend.
It handles application lifecycle, middleware setup, route registration, and server configuration.

Key Features:
- RESTful API endpoints for e-commerce operations
- CORS middleware for cross-origin requests
- Database connection management
- Health check endpoints
- Production-ready configuration

Author: AI E-Commerce Platform Team
Version: 1.0.0
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Add the current directory to Python path for relative imports
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import application components
from config.settings import settings
from config.database import create_tables
from controllers.product_controller import ProductController


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan management for startup and shutdown events.
    
    This context manager handles:
    - Database table creation on startup
    - Graceful shutdown procedures
    - Resource cleanup
    
    Args:
        app (FastAPI): The FastAPI application instance
    """
    # Startup procedures
    print("Starting AI E-Commerce Platform...")
    await create_tables()
    print("Database tables initialized successfully")
    
    yield  # Application runs here
    
    # Shutdown procedures
    print("Shutting down AI E-Commerce Platform...")


def create_app() -> FastAPI:
    """
    Application factory pattern for creating FastAPI instance.
    
    This function:
    - Configures the FastAPI application with metadata
    - Sets up CORS middleware for cross-origin requests
    - Registers API route controllers
    - Defines health check endpoints
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    
    # Create FastAPI application with comprehensive metadata
    app = FastAPI(
        title="AI E-Commerce Platform",
        description="FastAPI-based e-commerce platform with AI capabilities including ChatGPT integration and ML analytics",
        version="1.0.0",
        docs_url="/docs",  # Swagger UI documentation
        redoc_url="/redoc",  # ReDoc documentation
        lifespan=lifespan
    )
    
    # Configure CORS middleware for cross-origin requests
    # This allows the Streamlit frontend to communicate with the FastAPI backend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,  # Frontend URLs
        allow_credentials=True,  # Allow cookies and authentication headers
        allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE)
        allow_headers=["*"],  # Allow all headers
    )
    
    # Register API route controllers with versioned prefixes
    app.include_router(
        ProductController().router, 
        prefix="/api/v1/products", 
        tags=["products"]
    )
    
    @app.get("/", tags=["root"])
    async def root():
        """
        Root endpoint providing basic API information.
        
        Returns:
            dict: API name and version information
        """
        return {
            "message": "AI E-Commerce Platform API", 
            "version": "1.0.0",
            "documentation": "/docs",
            "features": ["Product Management", "AI Chat Support", "ML Analytics"]
        }
    
    @app.get("/health", tags=["health"])
    async def health_check():
        """
        Health check endpoint for monitoring and load balancing.
        
        Returns:
            dict: Service health status
        """
        return {
            "status": "healthy", 
            "service": "e-commerce-api",
            "version": "1.0.0"
        }
    
    return app


# Create the FastAPI application instance
app = create_app()

if __name__ == "__main__":
    """
    Development server startup configuration.
    
    This block runs when the file is executed directly (not imported).
    Starts the Uvicorn ASGI server with development settings.
    """
    import uvicorn
    
    print("Starting FastAPI development server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Listen on all network interfaces
        port=8001,       # Use port 8001 (8000 is used by ML API)
        reload=True,     # Auto-reload on code changes
        log_level="info" # Detailed logging
    )