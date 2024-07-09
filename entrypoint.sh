#!/bin/sh

echo "Waiting for postgres..."

TMP_DATABASE_URL='flasker.postgres.database.azure.com'

echo "Database URL is $TMP_DATABASE_URL"

while ! nc -z $TMP_DATABASE_URL 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py run -h 0.0.0.0