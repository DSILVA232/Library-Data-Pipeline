# Schema design decisions

## Why Snowflake schema instead of Star schema

Project 1 used a star schema because the goal was analytical query performance and flat denormalised dimensions mean fewer joins and faster reads, which suits a BI heavy workload. This project on the other hand deliberately uses a Snowflake schema to contrast that decision and demonstrate that schema design should follow the shape of the data, not a default preference.

The library dataset has dimensions that contain genuine sub entities. A book has an author, and an author is a real independent entity with its own attributes. A book has a genre and a publisher etc. A member has a location, and location is shared across many members. Collapsing all of that into flat dimension tables would introduce redundancy: the same author name repeated on every book row, the same city repeated on every member row. The Snowflake schema removes that redundancy by giving each sub-entity its own table and linking via foreign key.

The trade off is more joins at query time. That is acceptable here because the dataset is small and the goal is schema correctness over read performance.

---

## Fact table 

A loan is the central measurable event in this system. It has a date, a duration, a potential fee, and it connects three entities: a member, a book, and a staff member at a specific point in time.

`loan_date`, `due_date`, `return_date`, and `late_fee` all stay in the fact table because they describe the loan event itself, not any of the entities involved. Nothing was extracted from this table.

A `dim_date` table (with columns like `day_of_week`, `month`, `quarter`, `is_weekend`) was considered and is standard practice in production warehouses and would let you group loans by time periods without performing complex date quieries buy in the end i decided against it here because the dataset is small and three date foreign keys pointing at the same dimension adds join complexity for little gain. This would be the first thing added if this pipeline were scaled up.

---

## Dimension tables

**dim_book** keeps title, ISBN, year published, and total copies, all attributes that directly describe the book itself. Author, genre, and publisher were extracted into their own tables because each is an independent entity: an author can write many books, a genre applies to many books, a publisher publishes many books. Storing them as raw strings in `dim_book` would repeat the same author name across every book row, which is the redundancy Snowflake schema exists to remove.

**dim_member** keeps full name, phone, address line, date of birth, membership date, and membership status. City, state, and postcode were extracted into `dim_location` because location is a shared sub entity, many members can live in the same city, and the city/state/postcode combination is a connected unit that belongs together. `address` (the street line) stays in `dim_member` because it is specific to each member, not shared.

`membership_date` stays in `dim_member` because it is a fixed fact about when this member joined, it never changes. `membership_status` also stays as the current value, but this column is the candidate for a dbt snapshot to track historical changes (e.g. a member moving from active to suspended). The column stays in the table; the snapshot handles the history.

**dim_staff** keeps full name and hire date as direct attributes. Branch and role were extracted into their own tables because both are shared entities, a branch has many staff, a role applies to many staff, and both are worth querying independently (e.g. how many staff per branch, what roles exist).

**dim_location** holds city, state, and postcode together. These three were not split further. Postcode already functionally determines city and state, so they are one coherent unit rather than three separate entities.

---

## The staff connection to fact_loans

This was a deliberate design decision that warrants explanation because the connection wasnt originally in the laons table and is not as obvious as member or book.

Three options were considered:

**Option 1: staff processed the loan.** `staff_id` sits on `fact_loans` representing the staff member who handled the transaction at checkout. This requires a business rule: every loan was processed by exactly one staff member. For a library this is reasonabl scenario wehre someone checks the book out at the desk. This is the option used in this schema, and the assumption is documented in the DDL.

**Option 2: staff connects through branches, not loans.** Staff are linked to branches, branches hold books, and staff have no direct presence on the fact table. In this model a separate fact table (`fact_staff_shifts` or similar) would handle staff activity if it were ever needed. 

**Option 3: staff as a standalone dimension.** A dimension table does not have to connect to the fact table. `dim_staff` could exist purely to describe the people who work in the library — supporting headcount or staffing reports, without appearing as a FK anywhere in `fact_loans`.

Option 1 was chosen to keep staff connected to the central pipeline and demonstrate a four way fact table join. The assumption is noted in the DDL as a business rule, not treated as an implicit truth.
