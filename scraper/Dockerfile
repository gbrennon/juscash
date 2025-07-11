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

RUN groupadd -r appuser && useradd -r -g appuser appuser

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libc6-dev \
        curl \
        cron \
    && curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION \
    && ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --chown=appuser:appuser scraper/pyproject.toml scraper/poetry.lock ./
COPY --chown=appuser:appuser scraper/alembic.ini ./

RUN poetry config virtualenvs.create false \
    && poetry install --only=main --no-dev \
    && rm -rf $POETRY_CACHE_DIR

RUN playwright install --with-deps

COPY --chown=appuser:appuser scraper/ ./

COPY --chown=appuser:appuser scraper/cron/cronjob /etc/cron.d/scraper-cron

RUN chmod 0644 /etc/cron.d/scraper-cron \
    && crontab /etc/cron.d/scraper-cron \
    && mkdir -p logs \
    && touch /var/log/cron.log

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import asyncio; import sys; sys.exit(0)"

COPY --chown=appuser:appuser scraper/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
