#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER myuser WITH PASSWORD 'mypassword';
    CREATE DATABASE mydatabase OWNER myuser;
    GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
EOSQL
