"""
Main FastAPI application entry point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.settings import settings
from config.database import create_tables
from controllers.product_controller import ProductController
from controllers.order_controller import OrderController
from controllers.user_controller import UserController
from controllers.cart_controller import CartController


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    await create_tables()
    yield
    # Shutdown


def create_app() -> FastAPI:
    """Application factory"""
    
    app = FastAPI(
        title="AI E-Commerce Platform",
        description="FastAPI-based e-commerce platform with AI capabilities",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(ProductController().router, prefix="/api/v1/products", tags=["products"])
    app.include_router(OrderController().router, prefix="/api/v1/orders", tags=["orders"])
    app.include_router(UserController().router, prefix="/api/v1/users", tags=["users"])
    app.include_router(CartController().router, prefix="/api/v1/cart", tags=["cart"])
    
    @app.get("/")
    async def root():
        return {"message": "AI E-Commerce Platform API", "version": "1.0.0"}
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "e-commerce-api"}
    
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )