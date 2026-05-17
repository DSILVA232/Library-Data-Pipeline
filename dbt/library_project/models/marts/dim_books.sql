SELECT 
    book_id,
    title,
    a.author_id,
    ISBN,
    g.genre_id,
    p.publisher_id,
    year_published,
    total_copies
FROM {{ref('stg_books')}} AS b

LEFT JOIN {{ref('dim_author')}} AS a 
    ON b.author = a.author_name

LEFT JOIN {{ref('dim_genre')}} AS g 
    ON b.genre = g.genre_name

LEFT JOIN {{ref('dim_publisher')}} AS p 
    ON b.publisher = p.publisher_name
