# Juscash scraper

A web scraping package developed for Juscash assessment.

## Installation

This project uses Poetry for dependency management. Make sure you have Poetry installed on your system.

### Requirements

- Python 3.12+
- Poetry

### Setup

1. Install dependencies:
```bash
poetry install
```

2. Set up development environment (optional):
```bash
poetry run pre-commit install
```

## Usage

### Basic Usage

```python
from scraper import Scraper

# Create scraper instance
scraper = Scraper()

# Use the scraper
# Add your usage examples here
```

### Running the Scraper

```bash
# Activate the virtual environment
poetry shell

# Run your scraper script
```

### Generating Migrations
```bash
poetry run alembic revision --autogenerate -m "Initial migration"
```

### Applying Migrations
```bash
poetry run alembic -c scraper/alembic.ini upgrade head
```

## Development

This project follows strict code quality standards:

### Code Quality Tools

- **Ruff**: Linting and code formatting
- **MyPy**: Static type checking
- **Pre-commit**: Git hooks for quality assurance

### Development Workflow

1. **Format code**:
```bash
poetry run ruff format .
```

2. **Check linting**:
```bash
poetry run ruff check .
```

3. **Type checking**:
```bash
poetry run mypy .
```

### Pre-commit Hooks

Pre-commit hooks automatically run quality checks on every commit:
- Code formatting (Ruff)
- Linting (Ruff)
- Type checking (MyPy)
- Basic file checks (trailing whitespace, file endings, etc.)

## Project Structure

```
scraper/
├── src/
│   └── scraper/
│       ├── __init__.py
│       └── main.py
├── pyproject.toml
├── .pre-commit-config.yaml
└── README.md
```

## Configuration

All project configuration is centralized in `pyproject.toml`:
- Poetry dependencies
- Ruff linting and formatting settings
- MyPy type checking configuration
- Pre-commit hook settings

## License

[Add your license here]

## Assessment Notes

This project was developed as part of the Juscash technical assessment, demonstrating:
- Modern Python development practices
- Code quality standards
- Professional project structure
- Type safety and linting# Juscash scraper
