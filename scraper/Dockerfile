FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    PYTHONPATH=/app

# Create app user/group early
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install system deps and Poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libc6-dev \
        curl \
    && curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION \
    && ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first for better cache usage
COPY --chown=appuser:appuser scraper/pyproject.toml scraper/poetry.lock ./
COPY --chown=appuser:appuser scraper/alembic.ini ./

RUN poetry config virtualenvs.create false \
    && poetry install --only=main --no-dev \
    && rm -rf $POETRY_CACHE_DIR

# Copy application code
COPY --chown=appuser:appuser scraper/ ./

# Create logs directory as the correct user
RUN mkdir -p logs

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import asyncio; import sys; sys.exit(0)"

CMD ["python", "src/main.py"]
