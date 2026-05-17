SELECT 
    member_id,
    full_name,
    phone,
    address,
    date_of_birth,
    membership_date,
    membership_status,
    l.location_id,
    ingestion_timestamp
FROM {{ref('stg_members')}} AS m

LEFT JOIN {{ref('dim_location')}} AS l
    ON m.city = l.city AND m.state = l.state AND m.postcode = l.postcode 

