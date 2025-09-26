# ---------------------
# Base image with Python 3.12
# ---------------------
# Start from the smallest recommended image
FROM python:3.12-slim AS base

# Install curl (needed for uv installer) and clean up cache immediately
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Set up uv environment variables
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /app
ENV UV_PROJECT_ENV=/app/.venv


# ---------------------
# Dependencies stage (Build Stage)
# ---------------------
FROM base AS deps

# Install build tools (gcc) and uv
# Note: These tools are large but will NOT be in the final 'runtime' image.
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && rm -rf /var/lib/apt/lists/*

# Copy project metadata (uv.lock should be frozen to guarantee reproducibility)
COPY pyproject.toml uv.lock* ./

# Install dependencies (prod only, frozen from lockfile)
# This creates the virtual environment at /app/.venv
RUN uv sync


# ---------------------
# Runtime stage (Final Image)
# ---------------------
# Use the same minimal base image for consistency and smallest possible size
FROM base AS runtime

WORKDIR /app

# *** CRITICAL: Copy ONLY the virtual environment and source code ***
# This step does NOT include the large build tools (gcc, etc.) from 'deps' stage.
COPY --from=deps /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy application source code (your local directory)
# This should be the last step to optimize Docker build caching.
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI via uvicorn
# Note: Ensure 'fastapi' is installed via uv if you use this command, 
# or use 'uvicorn <module>:<app> --host 0.0.0.0 --port 8000'
CMD ["fastapi", "run", "api.py"]