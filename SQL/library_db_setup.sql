CREATE OR REPLACE TABLE raw.members (
    member_id              INTEGER,
    full_name              VARCHAR,
    email                  VARCHAR,
    phone                  VARCHAR,
    address                VARCHAR,
    city                   VARCHAR,
    state                  VARCHAR,
    postcode               VARCHAR,
    date_of_birth          DATE,
    membership_date        DATE,
    membership_status      VARCHAR,
    ingestion_timestamp    TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    source_file            VARCHAR
);


CREATE OR REPLACE TABLE raw.books (
    book_id                INTEGER,
    title                  VARCHAR,
    author                 VARCHAR,
    isbn                   VARCHAR,
    genre                  VARCHAR,
    publisher              VARCHAR,
    year_published         INTEGER,
    total_copies           INTEGER,
    ingestion_timestamp    TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    source_file            VARCHAR
);



CREATE OR REPLACE TABLE raw.loans (
    loan_id                INTEGER,
    member_id              INTEGER,
    book_id                INTEGER,
    loan_date              DATE,
    due_date               DATE,
    return_date            DATE,
    is_late                BOOLEAN,
    staff_id               INTEGER,
    ingestion_timestamp    TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    source_file            VARCHAR
);



CREATE OR REPLACE TABLE raw.staff (
    staff_id               INTEGER,
    full_name              VARCHAR,
    branch                 VARCHAR,
    role                   VARCHAR,
    hire_date              DATE,
    ingestion_timestamp    TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    source_file            VARCHAR
);