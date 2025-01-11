# Rebate-Management-System

A rebate management system that handles rebate program data, calculates rebates, and provides endpoints for basic
reporting

## Steps to generate version file on schema change

1. Navigate to folder "src/"
2. Autogenerate \
   Set env variables
    ```aiignore
    export DB_USERNAME=postgres
    export DB_PASSWORD=postgres
    export DB_HOST=0.0.0.0
    export DB_PORT=5432
    export DB_NAME=rebate
    ```
   Run
    ```
    alembic -c src/config/alembic.ini revision --autogenerate -m "Create ..."
    ```
   Above command creates a version prefix python script in src/db/migration/version

3. Manual
    ```aiignore
    alembic -c src/config/alembic.ini revision -m "Create ..."
    ```
