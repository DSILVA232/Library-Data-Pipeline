# PySpark — Data Cleaning & Transformation

## Pipeline pattern: EtLT

This project follows an EtLT pattern — Extract, lightweight transform, Load, then Transform.

PySpark handles the lightweight `t` — reading the raw CSV source files and cleaning them before anything touches the warehouse. This means fixing column names, standardising date formats, handling nulls, removing duplicates, and correcting data types. The goal at this stage is not to interpret the data, just to make it trustworthy and loadable. The output is clean Parquet files written to AWS S3.

The heavy `T` happens later in dbt, inside Snowflake, where the clean flat data gets shaped into the dimensional model — facts, dimensions, surrogate keys, and business logic.

The boundary between the two is intentional: PySpark answers "is this data correct?", dbt answers "what does this data mean?"


## upload note

This pipeline is designed as a full refresh pipeline. On each run, the target S3 bucket prefix is cleared using the clear_s3_prefix function before new files are uploaded via the upload_folder function. This was an intentional design decision.

Without this approach, every pipeline execution would generate new parquet filenames even when the underlying data had not changed. Since Spark outputs files with dynamically generated names, identical datasets would still appear as new objects in S3. When loaded into Snowflake, this would result in duplicate records being ingested.

An alternative approach that was considered was using the PURGE option within the Snowflake COPY INTO command. However, this would not fully solve the issue. While PURGE removes files from the S3 stage after ingestion, the duplicate data would have already been loaded into Snowflake. Because of this, the issue is more effectively addressed at the upload stage rather than during ingestion.

The primary drawback of the full refresh approach is the loss of historical raw data. For this project, that trade off is acceptable because the pipeline is designed around a one time ingestion scenario where the raw dataset moves through the pipeline only once.

That said the very idea of data engineering pipe lines revolves around there being constatn scheduled runs and many aspects of this project were intentionally designed with scalable and incrementally growing datasets in mind. So for those who wish to retain historical data while avoiding duplicate ingestion and be able to take full advantage of this pipeline, the following aproaches are recommended:

-Ensure only genuinely new data is processed
-After successful upload, either:
    remove local files that have already been uploaded, or
    move processed files into an archive directory so the upload directory contains only new data
-Implement deduplication logic within Snowflake

Most of the foundation for this incremental approach already exists within the project architecture. Only minor adjustments to the DBT models and COPY INTO scripts would be required to support it fully.