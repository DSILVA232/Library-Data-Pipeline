
USE ROLE ACCOUNTADMIN;


CREATE ROLE IF NOT EXISTS engineer;
CREATE ROLE IF NOT EXISTS analyst;


-- assign roles to you're self in order to allow future scripts + analytics to run smoothly
-- to find our you're current user SELECT CURRENT_USER();
-- To display you're current user roles  SHOW GRANTS TO USER <CURRENTUSER>
GRANT ROLE engineer TO USER <CURRENTUSER>;
GRANT ROLE analyst TO USER  <CURRENTUSER>;


-- Create Wharehouse
CREATE WAREHOUSE IF NOT EXISTS development
WITH
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 30
    AUTO_RESUME = true;

USE WAREHOUSE development;

-- Grant wharehouse usage 
GRANT USAGE ON WAREHOUSE development TO ROLE engineer;
GRANT USAGE ON WAREHOUSE development TO ROLE analyst;

-- Create Database
CREATE DATABASE IF NOT EXISTS LIBRARY_DB;

--Create Schemas
CREATE SCHEMA IF NOT EXISTS LIBRARY_DB.raw WITH MANAGED ACCESS;
CREATE SCHEMA IF NOT EXISTS LIBRARY_DB.staging WITH MANAGED ACCESS ;
CREATE SCHEMA IF NOT EXISTS LIBRARY_DB.marts WITH MANAGED ACCESS ;


-- ACCESS CONTROL

-- engineers: full control of RAW + STAGING
GRANT USAGE ON DATABASE LIBRARY_DB TO ROLE engineer;
GRANT ALL ON SCHEMA LIBRARY_DB.raw TO ROLE engineer;
GRANT ALL ON SCHEMA LIBRARY_DB.staging TO ROLE engineer;
GRANT ALL ON SCHEMA LIBRARY_DB.marts TO ROLE engineer;


-- analysts: read marts only
GRANT USAGE ON DATABASE LIBRARY_DB TO ROLE analyst;
GRANT USAGE ON SCHEMA LIBRARY_DB.marts TO ROLE analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA LIBRARY_DB.marts TO ROLE analyst;
GRANT SELECT ON FUTURE TABLES IN SCHEMA LIBRARY_DB.marts TO ROLE analyst;


CREATE STORAGE INTEGRATION s3_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = '<YOUR_AWS_ROLE_ARN>' -- to find this follow the documenation provided by the link in the SQL/README
  STORAGE_ALLOWED_LOCATIONS = ('<YOUR_S3_BUCKET_URL>'); -- to find this follow the documenation provided by the link in the SQL/README


CREATE OR REPLACE FILE FORMAT my_parquet_format
TYPE = PARQUET;


CREATE OR REPLACE STAGE my_s3_stage
    STORAGE_INTEGRATION = S3_INTEGRATION
    URL = '<YOUR_S3_BUCKET_URL>/raw/' -- to find this follow the documenation provided by the link in the SQL/README
    FILE_FORMAT = my_parquet_format;







CREATE OR REPLACE TABLE raw.members (
    member_id              INTEGER,
    full_name              VARCHAR,
    email                  VARCHAR,
    phone                  VARCHAR,
    address                VARCHAR,
    city                   VARCHAR,
    state                  VARCHAR,
    postcode               VARCHAR,
    date_of_birth          DATE,
    membership_date        DATE,
    membership_status      VARCHAR,
    ingestion_timestamp    TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    source_file            VARCHAR
);


CREATE OR REPLACE TABLE raw.books (
    book_id                INTEGER,
    title                  VARCHAR,
    author                 VARCHAR,
    isbn                   VARCHAR,
    genre                  VARCHAR,
    publisher              VARCHAR,
    year_published         INTEGER,
    total_copies           INTEGER,
    ingestion_timestamp    TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    source_file            VARCHAR
);



CREATE OR REPLACE TABLE raw.loans (
    loan_id                INTEGER,
    member_id              INTEGER,
    book_id                INTEGER,
    loan_date              DATE,
    due_date               DATE,
    return_date            DATE,
    is_late                BOOLEAN,
    staff_id               INTEGER,
    ingestion_timestamp    TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    source_file            VARCHAR
);



CREATE OR REPLACE TABLE raw.staff (
    staff_id               INTEGER,
    full_name              VARCHAR,
    branch                 VARCHAR,
    role                   VARCHAR,
    hire_date              DATE,
    ingestion_timestamp    TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    source_file            VARCHAR
);