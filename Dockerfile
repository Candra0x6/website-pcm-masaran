FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PORT=8000

WORKDIR /app

RUN useradd -u 1000 -m -s /bin/bash appuser

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

RUN mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app && \
    chmod +x /app/entrypoint.sh

USER appuser
RUN uv run python manage.py collectstatic --no-input

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["sh", "-c", "uv run gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2"]
