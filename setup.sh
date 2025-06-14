#!/bin/bash

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Create Initial data..."
python manage.py create_default_superuser
python manage.py create_roles
python manage.py create_user_with_admin_role 

echo "🚀 Starting Gunicorn server..."
gunicorn task_tracker.wsgi:application --bind 0.0.0.0:8000 -w 3 --timeout 120

