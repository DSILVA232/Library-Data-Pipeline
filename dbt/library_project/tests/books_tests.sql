SELECT *
FROM {{ref('dim_books')}}
WHERE total_copies < 0 

UNION ALL

SELECT *
FROM {{ref('dim_books')}}
WHERE year_published > YEAR(CURRENT_DATE)