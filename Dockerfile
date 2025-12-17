# Use a slim Python base image for a lightweight final image
FROM python:3.13-slim AS builder

# Set environment variables for Python and uv
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_CACHE_DIR="/root/.cache/uv" \
    UV_PROJECT="/app"

# Install system dependencies required by uv and potentially by Python packages
RUN apt-get update && \
    apt-get install --no-install-recommends -y curl git && \
    rm -rf /var/lib/apt/lists/*

# Copy the uv and uvx executables directly from the official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set up the working directory
WORKDIR /app

# Copy the dependency files first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./

# Install only the project dependencies (excluding the project itself) using uv sync
# The --frozen flag ensures the lockfile is not modified, and cache is used for performance
RUN --mount=type=cache,target=$UV_CACHE_DIR \
    --mount=type=bind,source=uv.lock,target=uv.lock,ro \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml,ro \
    uv sync --frozen --no-install-project

# Final stage: Create the production image
FROM python:3.13-slim AS production

# Set environment variables for Python and the application
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_DIR="/app"

# Create a non-root user for security
ARG APP_USER=appuser
ARG APP_UID=1001
ARG APP_GID=1001
RUN addgroup --gid $APP_GID $APP_USER && \
    adduser -h $APP_DIR -u $APP_UID -G $APP_USER -D $APP_USER

# Set the working directory
WORKDIR $APP_DIR

# Copy the application code from the build context
COPY --chown=$APP_UID:$APP_GID . .

# Copy the pre-installed virtual environment from the builder stage
COPY --from=builder $APP_DIR/.venv $APP_DIR/.venv

# Add the virtual environment's bin directory to the PATH
ENV PATH="$APP_DIR/.venv/bin:$PATH"

# Switch to the non-root user
USER $APP_UID:$APP_GID

# Expose the port the application will listen on
EXPOSE 8000

# Run the FastAPI application using uv run and uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]