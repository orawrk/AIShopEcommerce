"""
User controller for handling HTTP requests
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..config.database import get_database
from ..services.user_service import UserService
from ..schemas.user_schemas import (
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema,
    UserLoginSchema,
    TokenSchema
)


class UserController:
    """User controller for API endpoints"""
    
    def __init__(self):
        self.router = APIRouter()
        self._register_routes()
    
    def _register_routes(self):
        """Register all user routes"""
        
        @self.router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
        async def register_user(
            user_data: UserCreateSchema,
            db: Session = Depends(get_database)
        ):
            """Register a new user"""
            try:
                # Check if user already exists
                existing_user = UserService.get_user_by_username(db, user_data.username)
                if existing_user:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Username already registered"
                    )
                
                existing_email = UserService.get_user_by_email(db, user_data.email)
                if existing_email:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already registered"
                    )
                
                user = UserService.create_user(db, user_data)
                return user
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to create user: {str(e)}"
                )
        
        @self.router.post("/login", response_model=TokenSchema)
        async def login_user(
            login_data: UserLoginSchema,
            db: Session = Depends(get_database)
        ):
            """Authenticate user and return token"""
            user = UserService.authenticate_user(db, login_data.username, login_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            access_token = UserService.create_access_token({"sub": user.username})
            return TokenSchema(access_token=access_token)
        
        @self.router.get("/me", response_model=UserResponseSchema)
        async def get_current_user(
            current_user = Depends(UserService.get_current_user)
        ):
            """Get current user profile"""
            return current_user
        
        @self.router.put("/me", response_model=UserResponseSchema)
        async def update_current_user(
            user_data: UserUpdateSchema,
            current_user = Depends(UserService.get_current_user),
            db: Session = Depends(get_database)
        ):
            """Update current user profile"""
            user = UserService.update_user(db, current_user.id, user_data)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            return user