FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements-api.txt .
COPY requirements-worker.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --user -r requirements-worker.txt

# Final stage
FROM python:3.11-slim AS runtime

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 osint && \
    mkdir -p /reports && \
    chown -R osint:osint /app /reports

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/osint/.local
ENV PATH=/home/osint/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy application code
COPY --chown=osint:osint . .

USER osint

# Celery doesn't have a built-in healthcheck like uvicorn, 
# but we can check if the process is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD pgrep -f "celery" || exit 1

# Start Celery worker
CMD ["celery", "-A", "app.tasks.celery_app", "worker", "--loglevel=info"]
