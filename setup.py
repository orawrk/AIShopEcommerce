"""
Setup script for AI-Powered E-Commerce Platform
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-ecommerce-platform",
    version="1.0.0",
    author="AI E-Commerce Platform Team",
    author_email="team@example.com",
    description="AI-powered e-commerce platform with ChatGPT integration and ML analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-ecommerce-platform",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Framework :: FastAPI",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Office/Business :: Financial :: Point-Of-Sale",
    ],
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "sqlalchemy>=2.0.23",
        "pymysql>=1.1.0",
        "streamlit>=1.28.2",
        "plotly>=5.17.0",
        "pandas>=2.1.4",
        "numpy>=1.25.2",
        "scikit-learn>=1.3.2",
        "openai>=1.3.8",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "requests>=2.31.0",
        "python-multipart>=0.0.6",
        "cryptography>=41.0.8",
        "bcrypt>=4.1.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.7.0",
        ],
        "production": [
            "gunicorn>=21.2.0",
            "psycopg2-binary>=2.9.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "ecommerce-backend=backend.main:main",
            "ecommerce-ml=ml_api:main",
            "ecommerce-seed=backend.seed_data:main",
        ],
    },
)