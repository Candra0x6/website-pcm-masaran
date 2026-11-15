#!/bin/sh
set -e

echo "Menjalankan migrasi database..."
uv run python manage.py migrate --no-input

exec "$@"
