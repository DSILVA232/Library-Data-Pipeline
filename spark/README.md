# PySpark — Data Cleaning & Transformation

## Pipeline pattern: EtLT

This project follows an EtLT pattern — Extract, lightweight transform, Load, then Transform.

PySpark handles the lightweight `t` — reading the raw CSV source files and cleaning them before anything touches the warehouse. This means fixing column names, standardising date formats, handling nulls, removing duplicates, and correcting data types. The goal at this stage is not to interpret the data, just to make it trustworthy and loadable. The output is clean Parquet files written to AWS S3.

The heavy `T` happens later in dbt, inside Snowflake, where the clean flat data gets shaped into the dimensional model — facts, dimensions, surrogate keys, and business logic.

The boundary between the two is intentional: PySpark answers "is this data correct?", dbt answers "what does this data mean?"
