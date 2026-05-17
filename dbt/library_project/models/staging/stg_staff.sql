SELECT
    staff_id,
    full_name,
    branch,
    role,
    hire_Date,
    ingestion_timestamp,
    source_file
FROM {{source('library','STAFF')}}