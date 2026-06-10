#!/bin/bash
# Stop execution if any command fails
set -e

echo "Waiting for PostgreSQL to wake up..."
until pg_isready -h "$RSSA_DB_HOST" -U "$RSSA_DB_USER"; do
  echo "PostgreSQL is unavailable - sleeping..."
  sleep 2
done
echo "PostgreSQL is ready!"

echo "Running Alembic migrations..."
(cd src/rssa_storage/rssadb && uv run alembic upgrade head)
(cd src/rssa_storage/moviedb && uv run alembic upgrade head)
(cd src/rssa_storage/telemetrydb && uv run alembic upgrade head)

echo "Seeding the database..."
(bash scripts/seed_local_moviedb.sh)

echo "Migrations and seeding complete! Shutting down migrator."
