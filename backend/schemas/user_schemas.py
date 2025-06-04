"""
User-related Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from ..models.enums import UserRoleEnum


class UserBaseSchema(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


class UserCreateSchema(UserBaseSchema):
    """User creation schema"""
    password: str = Field(..., min_length=8)
    role: UserRoleEnum = UserRoleEnum.CUSTOMER


class UserUpdateSchema(BaseModel):
    """User update schema"""
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


class UserResponseSchema(UserBaseSchema):
    """User response schema"""
    id: int
    is_active: bool
    role: UserRoleEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    """User login schema"""
    username: str
    password: str


class TokenSchema(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"