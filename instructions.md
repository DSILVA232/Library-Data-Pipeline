# Instructions

## Prerequisites

- Python 3.11
- Docker and Docker Compose
- Java (required by PySpark locally) — `sudo apt-get install default-jdk`
- AWS account with S3 bucket
- Snowflake account
- Prefect Cloud account (free tier) — [app.prefect.io](https://app.prefect.io)
- dbt Core with Snowflake adapter — `pip install dbt-snowflake`

---

## 1. Clone the repository

```bash
git clone https://github.com/yourusername/library.git
cd library
```

---

## 2. Set up virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

---

## 3. Configure environment variables

Create a `.env` file in the project root:

```
# AWS
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=ap-southeast-2
AWS_BUCKET_NAME=your_bucket_name

# Snowflake
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=LIBRARY_DB
SNOWFLAKE_SCHEMA=RAW
```

This file is gitignored and should never be committed.

For full env file example look in .env-example fil in main dir : [.env_example](https://app.prefect.io)

---

## 4. Set up Snowflake infrastructure

Run the following SQL files in Snowflake in order:

```
sql/library_db_setup.sql      — creates database, schemas, warehouse
sql/storage_integration.sql   — creates S3 external stage integration
```

These are one-time setup scripts. After running them, update the IAM trust policy in AWS with the Snowflake IAM user ARN returned by:

```sql
DESC INTEGRATION s3_integration;
```

---

## 5. Set up dbt

```bash
cd dbt/library
dbt deps          # installs dbt_utils package
dbt debug         # confirms Snowflake connection is working
```

---

## 6. Connect to Prefect Cloud

```bash
prefect cloud login
```

Follow the browser prompt to authenticate with your Prefect Cloud account.

---

## 7. Generate raw data

```bash
python data_generation/generate.py
```

This generates the four raw CSV files in `data_raw/`.

---

## 8. Run the pipeline

```bash
python pipeline/flow.py
```

This triggers the full pipeline:
1. PySpark cleaning job via Docker
2. S3 upload
3. Snowflake COPY INTO
4. dbt snapshot
5. dbt run
6. dbt test

Monitor the run at [app.prefect.io](https://app.prefect.io).

---

## 9. Run tests

```bash
pytest tests/
```

Runs unit tests for all PySpark transform functions.

---

## Project structure

```
library/
  data_creation/
     fake_data.py
     README.md
  data_raw/           raw CSV files (gitignored)
  spark/
    output/           output paraqueet files gitignored
    cleaning.py       PySpark cleaning job
    s3_upload.py      boto3 S3 upload script
    README.md         EtLT pattern explanation
  profiling/
    profiling.py      ydata-profiling and manual checks
    profiling_report.md
    reports/          HTML profiling reports (gitignored)
  dbt/
    library_project/
      macros/
        generate_schema_name.sql  this makes sure outputed schema names to snowflake are correct
      models/
        staging/      one view per source table
        marts/        dimension and fact models
      snapshots/      SCD Type 2 snap_members
      tests/          custom SQL tests
  Prefect/
    flow.py           Prefect orchestration flow
  SQL/
    library_db_setup.sql
    ingestion.sql
  schema/
    DDL.sql           schema design reference (not executed)
    decisions.md
    snowflake_schema.jpg

  tests/ (coming soon)
    test_transforms.py  pytest unit tests (not yet added)
  docker/
    Dockerfile
    requirements.txt        pipeline dependencies
  compose.yaml
  requirements-dev.txt    full dev dependencies
  .env                    credentials (gitignored)
  .gitignore
  README.md
  Instructions.md
```
