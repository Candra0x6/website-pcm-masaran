# Base Image: Python 3.13 Slim resmi
FROM python:3.13-slim

# Install uv package manager resmi via multi-stage copy
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PORT=8000

# Set working directory
WORKDIR /app

# Buat non-root user 'appuser'
RUN useradd -u 1000 -m -s /bin/bash appuser

# Salin file spesifikasi dependensi uv
COPY pyproject.toml uv.lock ./

# Install dependensi menggunakan uv
RUN uv sync --frozen --no-dev

# Salin seluruh source code proyek
COPY . .

# Buat direktori staticfiles dan media, lalu berikan ownership ke non-root appuser
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app && \
    chmod +x /app/entrypoint.sh

# Jalankan collectstatic saat proses build image sebagai appuser
USER appuser
RUN uv run python manage.py collectstatic --no-input

# Expose port container
EXPOSE 8000

# Set entrypoint & command
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["sh", "-c", "uv run gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2"]
