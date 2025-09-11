#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Waiting for database to be ready..."
# This is a simple loop to wait for the DB to be available.
# A more robust solution might use a tool like wait-for-it.sh
until PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

# Run Alembic migrations
echo "Running Alembic revision..."
alembic revision --autogenerate -m "Initial migration from docker"

echo "Running Alembic upgrade..."
alembic upgrade head

echo "Migrations complete."
