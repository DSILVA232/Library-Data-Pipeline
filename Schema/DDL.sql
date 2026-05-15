CREATE TABLE location (
    id int NOT NULL PRIMARY KEY,
    city varchar(50),
    state varchar(50),
    postcode varchar(10)

);


CREATE TABLE members(
    id int NOT NULL PRIMARY KEY,
    full_name varchar(100),
    email varchar(50),
    phone varchar(20),
    address varchar(100),
    date_of_birth date,
    membership_date date,
    membership_status varchar(20) CHECK (membership_status IN ('Active', 'Inactive', 'Expired')),
    location_id int,
    CONSTRAINT FK_location FOREIGN KEY (location_id) REFERENCES location(id)

);


CREATE TABLE branch(
    id int NOT NULL PRIMARY KEY,
    branch_name varchar(50)


);


CREATE TABLE role(
    id int NOT NULL PRIMARY KEY,
    role_name varchar(50)


);


CREATE TABLE staff(
    id int NOT NULL PRIMARY KEY,
    full_name varchar(100),
    branch_id int,
    role_id int,
    hire_date date,
    CONSTRAINT FK_branch FOREIGN KEY (branch_id) REFERENCES branch(id),
    CONSTRAINT FK_role FOREIGN KEY (role_id) REFERENCES role(id)
    
);


CREATE TABLE author(
    id int NOT NULL PRIMARY KEY,
    author_name varchar(100)


);


CREATE TABLE genre(
    id int NOT NULL PRIMARY KEY,
    genre_name varchar(50)



);


CREATE TABLE publisher(
    id int NOT NULL PRIMARY KEY,
    publisher_name varchar(50)


);


CREATE TABLE books(
    id int NOT NULL PRIMARY KEY,
    title varchar(200),
    author_id int,
    isbn varchar(17) NOT NULL UNIQUE,
    genre_id int,
    publisher_id int,
    year_published int CHECK (year_published BETWEEN 1450 AND EXTRACT(YEAR FROM CURRENT_DATE)),
    total_copies int ,
    CONSTRAINT FK_author FOREIGN KEY (author_id) REFERENCES author(id),
    CONSTRAINT FK_genre FOREIGN KEY (genre_id) REFERENCES genre(id),
    CONSTRAINT FK_publisher FOREIGN KEY (publisher_id) REFERENCES publisher(id)

);


CREATE TABLE Loans(
    id int NOT NULL PRIMARY KEY,
    staff_id int,
    book_id int,
    loan_date date,
    due_date date CHECK (due_date > loan_date),
    return_date date CHECK (return_date >= loan_date),
    is_late boolean,
    member_id int,
    CONSTRAINT FK_staff FOREIGN KEY (staff_id) REFERENCES staff(id),
    CONSTRAINT FK_book FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE RESTRICT,
    CONSTRAINT FK_member FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE RESTRICT

);

