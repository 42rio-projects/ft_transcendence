#!/bin/sh

echo > ~/.pg_service.conf "[admin]
host=$DB_HOST
user=$DB_USER
dbname=$DB_NAME
port=$DB_PORT"

python manage.py runserver
