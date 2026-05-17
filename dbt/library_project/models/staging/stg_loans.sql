SELECT 
    loan_id,
    member_id,
    book_id,
    loan_date,
    due_date,
    return_date,
    is_late,
    staff_id,
    ingestion_timestamp,
    source_file
FROM {{source('library','LOANS')}}
