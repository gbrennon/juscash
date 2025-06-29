FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1

# Create app user (security best practice)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install system dependencies and Poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libc6-dev \
        curl \
    && pip install poetry==$POETRY_VERSION \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy Poetry configuration files and alembic.ini
COPY scraper/pyproject.toml scraper/poetry.lock ./
COPY scraper/alembic.ini ./

# Configure Poetry and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --only=main --no-dev \
    && rm -rf $POETRY_CACHE_DIR

# Copy the entire scraper project (excluding pyproject.toml, poetry.lock, alembic.ini already copied)
COPY scraper/src ./scraper/src
COPY scraper/tests ./scraper/tests
COPY scraper/README.md ./scraper/README.md

# Create logs directory
RUN mkdir -p logs && chown -R appuser:appuser logs

# --- ADD THIS LINE TO FIX PERMISSION ---
# Change ownership of the scraper source directory to appuser
RUN chown -R appuser:appuser scraper/src

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import asyncio; import sys; sys.exit(0)"

# Default command
CMD ["python", "-m", "scraper"]
