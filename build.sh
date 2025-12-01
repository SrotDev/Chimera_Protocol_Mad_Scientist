#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn dj-database-url whitenoise

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
