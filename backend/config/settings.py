"""
Application configuration settings
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings configuration"""
    
    # MySQL Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/ecommerce?unix_socket=/tmp/mysql.sock")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "3306"))
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "ecommerce")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "root")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "")
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "AI E-Commerce Platform"
    VERSION: str = "1.0.0"
    
    # Security Configuration
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Application Configuration
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()