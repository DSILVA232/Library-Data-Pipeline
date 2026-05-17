{{
    config(
        materialized='incremental',
        unique_key = 'loan_id'
    )
}}


SELECT
    l.loan_id,
    m.member_id,
    b.book_id,
    l.loan_date,
    l.due_date,
    l.return_date,
    l.is_late,
    s.staff_id,
    l.ingestion_timestamp
FROM {{ref('stg_loans')}} AS l

LEFT JOIN {{ref('dim_member')}} AS m
    ON l.member_id = m.member_id

LEFT JOIN {{ref('dim_books')}} AS b
    ON l.book_id = b.book_id

LEFT JOIN {{ref('dim_staff')}} AS s
    ON l.staff_id = s.staff_id



{% if is_incremental() %}

where l.ingestion_timestamp > (SELECT MAX(ingestion_timestamp) FROM {{ this }})

{% endif %}