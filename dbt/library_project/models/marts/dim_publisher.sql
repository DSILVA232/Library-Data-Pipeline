SELECT 
    {{ dbt_utils.generate_surrogate_key(['publisher']) }} AS publisher_id,
    publisher as publisher_name
FROM (
    SELECT DISTINCT publisher
    FROM {{ref('stg_books')}}
)