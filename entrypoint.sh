#!/bin/ash

echo "DB migration"
python manage.py migrate

exec "$@"

