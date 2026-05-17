SELECT
    member_id,
    full_name,
    email,
    phone,
    address,
    city,
    state,
    postcode,
    date_of_birth,
    membership_date,
    membership_status,
    ingestion_timestamp,
    source_file
FROM {{source('library','MEMBERS')}}