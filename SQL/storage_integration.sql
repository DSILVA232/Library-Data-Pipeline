CREATE STORAGE INTEGRATION s3_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::243746945243:role/library-eng-role'
  STORAGE_ALLOWED_LOCATIONS = ('s3://library-pipeline-243746945243-ap-southeast-2-an');



USE SCHEMA raw;

CREATE OR REPLACE FILE FORMAT my_parquet_format
TYPE = PARQUET;


CREATE OR REPLACE STAGE my_s3_stage
    STORAGE_INTEGRATION = S3_INTEGRATION
    URL = 's3://library-pipeline-243746945243-ap-southeast-2-an/raw/'
    FILE_FORMAT = my_csv_format;