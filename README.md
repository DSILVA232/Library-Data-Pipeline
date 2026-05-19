# Library Data Pipeline

An end to end EtLT pipeline built to ingest, clean, transform, and serve library data using a modern data stack. The focus of this project is the data engineering lifecycle — schema design, data quality, containerisation, and orchestration — with production minded engineering decisions at every stage.

The final output is a fully automated pipeline that ingests raw library data, cleans it at scale using PySpark, stages it in AWS S3, loads it into Snowflake, and transforms it into a normalised dimensional model using dbt. The pipeline terminates in a Power BI dashboard connected directly to Snowflake, demonstrating the data is queryable and useful for business reporting. Orchestrated end to end by Prefect and monitored via Prefect Cloud.

> **Local development** — install dependencies from `requirements-dev.txt` which includes profiling and development tools alongside the core pipeline dependencies. `requirements.txt` contains pipeline only dependencies used by Docker.

---

## Architecture

![Architecture Diagram](docs/architecture.png)

The pipeline follows an **EtLT pattern** — a lightweight transform before loading (PySpark handles data quality), followed by a heavier business logic transform inside the warehouse (dbt handles dimensional modelling). This is a deliberate design choice documented in the [Pipeline Pattern](spark/README.md).

---

## Schema

The warehouse uses a **Snowflake schema** (normalised dimensions) rather than a star schema. This decision was made because the library dataset has genuine sub-entities — books have authors, genres, and publishers; members have locations; staff have branches and roles. Collapsing these into flat dimensions would introduce redundancy. The full reasoning is documented in [Schema Decisions](Schema/decisions.md).

![Schema Diagram](docs/schema.png)

---

## Pipeline stages

Stages run sequentially, each dependent on the previous succeeding:

**1. run_spark** — PySpark job reads raw CSVs and performs structural cleaning: column name standardisation, date format normalisation, phone number standardisation, membership status standardisation, duplicate removal, and type casting. Outputs clean Parquet files locally.

**2. run_s3_upload** — boto3 script uploads clean Parquet files to AWS S3 under the `raw/` prefix. S3 acts as the staging layer between local compute and the warehouse.

**3. run_snowflake_ingestion** — Snowflake COPY INTO loads Parquet from S3 into the RAW schema via an external stage backed by a storage integration. Ingestion timestamp and source file metadata are added at load time.

**4. run_dbt_snapshot** — dbt snapshot captures historical changes to `dim_member` (membership status, address changes) using SCD Type 2. Runs before mart models to ensure history is captured before current state is overwritten.

**5. run_dbt_models** — dbt builds staging views and the full Snowflake schema: dimension tables with surrogate keys, an incremental `fact_loans` model that only processes new records on subsequent runs.

**6. run_dbt_tests** — dbt runs schema tests (not_null, unique, relationships, accepted_values) and custom SQL tests validating business logic (date integrity, is_late flag correctness, year published constraints).

---

## Data quality

Validation happens at two stages:

**Pre-load (PySpark)**
- Column name standardisation and typo correction
- Date format normalisation across multiple input formats → `YYYY-MM-DD`
- Phone number standardisation → `04XXXXXXXX`, 10 digit validation
- Membership status standardisation → `Active`, `Inactive`, `Expired`
- Duplicate detection with ID collision check before dropping
- Type casting with float intermediate to handle string encoded decimals

**Post-load (dbt)**
- `not_null` and `unique` on all primary keys
- `relationships` tests validating foreign key integrity across all dimension and fact tables
- `accepted_values` on `membership_status`
- Custom SQL tests: loan date integrity, is_late flag correctness, total copies non-negative, year published not in future

Any failure at either stage stops the pipeline — Prefect marks the task as failed and halts downstream execution.

---

## Materialisation strategy

| Model | Materialisation | Reason |
|---|---|---|
| fact_loans | incremental | append/update only new loan records on each run |
| dim_member | table | full refresh, current state |
| all other dims | table | small static lookup tables, full refresh |
| snap_members | snapshot | SCD Type 2 history of member status and address changes |

---

## Dataset

The library dataset is synthetically generated using the Faker library — no real personal data is used. The generation script produces four CSV files (members, books, loans, staff) with intentional data quality issues including inconsistent formats, duplicate records, missing values, and mixed value representations. This mirrors the kind of messy real world data a pipeline would typically encounter.

The dataset can be regenerated at any time to produce an identical or varied dataset. See [data_creation/README.md](data_creation/README.md) for full details on the generation script, the data model, and the intentional quality issues introduced.

---
## Project Setup

Note that before project can be automatically executed infrastrucute setup needs to be performed 
For full setup instructions see: [Instructions](Instructions.md)

```bash
# run the full pipeline
python pipeline/flow.py
```

The Prefect flow orchestrates all stages automatically. Monitor runs at [Prefect Cloud](https://app.prefect.io).

The pipeline is set to manual trigger only as the library dataset is a one time load. For continuous ingestion the Spark job and COPY INTO would run on a schedule.

---

## Tech stack

- **Python** — pipeline scripting and orchestration
- **PySpark** — distributed data cleaning and transformation
- **Docker** — containerised Spark execution
- **AWS S3** — staging layer between compute and warehouse
- **Snowflake** — cloud data warehouse
- **dbt** — SQL transformation, testing, and documentation
- **Prefect** — pipeline orchestration and monitoring
- **Power BI** — dashboard connected to Snowflake for business reporting
- **pytest** — unit testing for PySpark transform functions
- **GitHub Actions** — CI on pull requests

---

## Project decisions

- [Schema design decisions](Schema/decisions.md) — why Snowflake schema, how each table was designed, the staff connection decision, the date dimension tradeoff
- [Pipeline pattern](spark/README.md) — EtLT pattern explanation, where PySpark ends and dbt begins, why the boundary exists where it does
- [Data profiling report](profiling/profiling_report.md) — as-is analysis of each dataset before cleaning, findings that shaped the cleaning strategy

---

## Future improvements

- OpenLineage integration for data lineage tracking
- Expanded dbt tests with generic reusable test macros
- Alerting on pipeline failure via email or Slack
- Terraform for infrastructure as code (S3 bucket, Snowflake warehouse)
- Schedule based triggering via Prefect deployments
