#!/bin/bash
set -e

echo "Waiting for database..."
python -c "
import time, os, sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'partum_inventory.settings')
django.setup()
from django.db import connections
for i in range(30):
    try:
        connections['default'].ensure_connection()
        print('Database is ready!')
        sys.exit(0)
    except Exception:
        print(f'Waiting for database... attempt {i+1}/30')
        time.sleep(2)
print('Could not connect to database')
sys.exit(1)
"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec gunicorn partum_inventory.wsgi:application \
    --bind 0.0.0.0:8010 \
    --workers 3 \
    --access-logfile - \
    --error-logfile -
