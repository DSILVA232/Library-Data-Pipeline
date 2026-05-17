SELECT 
    {{ dbt_utils.generate_surrogate_key(['author']) }} AS author_id,
    author as author_name
FROM (
    SELECT DISTINCT author
    FROM {{ref('stg_books')}}
)