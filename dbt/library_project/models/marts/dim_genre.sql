SELECT 
    {{ dbt_utils.generate_surrogate_key(['genre']) }} AS genre_id,
    genre as genre_name
FROM (
    SELECT DISTINCT genre
    FROM {{ref('stg_books')}}
)