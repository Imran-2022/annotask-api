#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python manage.py migrate --no-input
python manage.py collectstatic --no-input
exec gunicorn config.wsgi:application
