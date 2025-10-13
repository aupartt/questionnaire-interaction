# Start with a suitable base image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /backend

COPY ./uv.lock ./pyproject.toml ./

# Set environment variables for UV
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# --no-dev to avoid installing dev dependencies in the final image
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

COPY ./app/ ./app/
COPY ./main.py .
COPY ./alembic/ ./alembic/
COPY alembic.ini .

# Set the PATH and PYTHONPATH for the application
ENV PATH="/backend/.venv/bin:$PATH"
ENV PYTHONPATH="/backend/"
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "-u", "-m", "main"]
