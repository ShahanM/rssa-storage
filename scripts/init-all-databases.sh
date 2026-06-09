#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE rssadb;
    CREATE DATABASE moviedb;
    CREATE DATABASE telemetrydb;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "moviedb" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS pg_trgm;
EOSQL
