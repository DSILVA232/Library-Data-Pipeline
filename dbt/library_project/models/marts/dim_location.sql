SELECT 
    {{ dbt_utils.generate_surrogate_key(['city','state','postcode']) }} AS location_id,
    city,
    state,
    postcode
FROM (
    SELECT DISTINCT city, state, postcode
    FROM {{ref('stg_members')}}
)