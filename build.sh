#!/usr/bin/env bash
# =============================================================================
# build.sh — Render Build Script for Sundari Silk Palace Backend
# =============================================================================
# This script runs automatically on every Render deployment.
# Render Build Command:  ./build.sh
# Render Start Command:  gunicorn config.wsgi:application --bind 0.0.0.0:$PORT

set -o errexit  # Exit immediately on any error

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Running database migrations..."
python manage.py migrate --no-input

echo "==> Seeding initial data (safe — uses get_or_create)..."
python manage.py seed_data

echo "==> Build complete!"
