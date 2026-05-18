## Snowflake Setup

Most of the setup code in `snowflake_setup.sql` was sourced directly from the official Snowflake documentation. Default choices were kept throughout, with two exceptions: Option 1 was used for configuring secure access to Amazon S3, and Parquet was used as the file format rather than CSV.

https://docs.snowflake.com/en/user-guide/data-load-s3

Before running the script, replace the following placeholders:

- `<CURRENTUSER>` — run `SELECT CURRENT_USER();` in Snowflake to find your username
- `<YOUR_AWS_ROLE_ARN>` — found in AWS IAM → Roles → your role → copy the ARN
- `<YOUR_S3_BUCKET_URL>` — found in AWS S3 → your bucket → copy the S3 URI (e.g. `s3://your-bucket-name`)