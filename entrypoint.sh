#!/bin/sh
set -e

# Jalankan migrasi database otomatis saat container web start
echo "Menjalankan migrasi database..."
uv run python manage.py migrate --no-input

# Jalankan perintah utama container (Gunicorn)
exec "$@"
