# Contributing to AI E-Commerce Platform

Thank you for your interest in contributing to the AI-powered e-commerce platform! This document provides guidelines for contributing to the project.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please be respectful and professional in all interactions.

## Getting Started

### Prerequisites

- Python 3.11+
- MySQL 8.0+
- Git
- Docker (optional)

### Development Setup

1. **Fork the repository**
```bash
git clone https://github.com/yourusername/ai-ecommerce-platform.git
cd ai-ecommerce-platform
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -e .
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
cd backend
python seed_data.py
```

6. **Run the development server**
```bash
# Terminal 1 - Backend
cd backend && python main.py

# Terminal 2 - ML API
python ml_api.py

# Terminal 3 - Frontend
streamlit run app.py --server.port 5000
```

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use type hints where possible
- Write docstrings for all functions and classes
- Keep functions focused and small
- Use meaningful variable and function names

### Commit Messages

Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat(backend): add user authentication endpoints
fix(frontend): resolve cart item duplication issue
docs(readme): update installation instructions
```

### Branch Naming

- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/documentation-update` - Documentation updates
- `refactor/component-name` - Code refactoring

### Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Maintain test coverage above 80%

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=backend tests/
```

## Project Structure

```
ai-ecommerce-platform/
├── backend/                # FastAPI backend
│   ├── controllers/        # API route handlers
│   ├── services/          # Business logic
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   └── config/            # Configuration
├── frontend/              # Streamlit application
├── ml/                    # Machine learning components
├── data/                  # Sample data
├── tests/                 # Test files
└── docs/                  # Documentation
```

## Contributing Process

### 1. Create an Issue

Before starting work, create an issue describing:
- The problem you're solving
- Your proposed solution
- Any breaking changes

### 2. Fork and Branch

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Write or update tests
5. Update documentation

### 3. Pull Request

1. Push your branch to your fork
2. Create a pull request to `main`
3. Fill out the PR template completely
4. Link related issues
5. Request review from maintainers

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Updated existing tests

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## Component Guidelines

### Backend (FastAPI)

- Use dependency injection for database sessions
- Implement proper error handling
- Follow REST conventions
- Use Pydantic for data validation
- Write comprehensive docstrings

Example:
```python
@router.post("/products/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_database)
) -> ProductResponse:
    """
    Create a new product.
    
    Args:
        product: Product data to create
        db: Database session
        
    Returns:
        Created product data
        
    Raises:
        HTTPException: If product creation fails
    """
    return ProductService.create_product(db, product)
```

### Frontend (Streamlit)

- Use session state for user data
- Implement proper error handling
- Follow Streamlit best practices
- Make UI responsive and intuitive

### Machine Learning

- Document model architecture
- Include model evaluation metrics
- Use proper data validation
- Implement model versioning

### Database

- Use proper migrations
- Index frequently queried columns
- Follow naming conventions
- Document schema changes

## Review Process

### Code Review Checklist

- [ ] Code is well-documented
- [ ] Tests are comprehensive
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Breaking changes documented
- [ ] Database migrations included (if needed)

### Review Timeline

- Initial review: 2-3 business days
- Follow-up reviews: 1-2 business days
- Urgent fixes: Same day

## Release Process

1. Create release branch from `main`
2. Update version numbers
3. Update CHANGELOG.md
4. Create pull request
5. Merge after approval
6. Tag release
7. Deploy to production

## Getting Help

- Check existing issues and documentation
- Join our discussions for questions
- Contact maintainers for urgent issues

## Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Invited to contributor events

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [MySQL Documentation](https://dev.mysql.com/doc/)

Thank you for contributing to the AI E-Commerce Platform!