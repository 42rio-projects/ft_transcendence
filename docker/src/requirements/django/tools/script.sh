#!/bin/sh

echo > ~/.pg_service.conf "[admin]
host=$DB_HOST
user=$DB_USER
password=$DB_PASSWORD
dbname=$DB_NAME
port=$DB_PORT"

python manage.py runserver 0.0.0.0:8000
