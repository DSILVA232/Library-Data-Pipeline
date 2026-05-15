COPY INTO raw.members
FROM @my_s3_stage/members/
PATTERN='.*[.]parquet'
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
INCLUDE_METADATA = (
    ingestion_timestamp = METADATA$START_SCAN_TIME,
    source_file = METADATA$FILENAME
)
ON_ERROR = 'ABORT_STATEMENT';


COPY INTO raw.books
FROM @my_s3_stage/books/
PATTERN='.*[.]parquet'
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
INCLUDE_METADATA = (
    ingestion_timestamp = METADATA$START_SCAN_TIME,
    source_file = METADATA$FILENAME
)
ON_ERROR = 'ABORT_STATEMENT';



COPY INTO raw.loans
FROM @my_s3_stage/loans/
PATTERN='.*[.]parquet'
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
INCLUDE_METADATA = (
    ingestion_timestamp = METADATA$START_SCAN_TIME,
    source_file = METADATA$FILENAME
)
ON_ERROR = 'ABORT_STATEMENT';



COPY INTO raw.staff
FROM @my_s3_stage/staff/
PATTERN='.*[.]parquet'
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
INCLUDE_METADATA = (
    ingestion_timestamp = METADATA$START_SCAN_TIME,
    source_file = METADATA$FILENAME
)
ON_ERROR = 'ABORT_STATEMENT';
 