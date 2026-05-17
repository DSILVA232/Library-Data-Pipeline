SELECT 
    book_id,
    title,
    author,
    ISBN,
    genre,
    publisher,
    year_published,
    total_copies,
    ingestion_timestamp,
    source_file
FROM {{source('library','BOOKS')}}