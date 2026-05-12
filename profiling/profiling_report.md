# Data Profiling Report

Each dataset was profiled individually using ydata profiling to establish a as is view of the data before any cleaning is applied. Findings are documented below and form the basis of the PySpark cleaning strategy.

---

## Data Type Audit

All columns are ingested as `string` by default. The target types below represent what each column should be cast to after cleaning.

### Members
| Column | Current Type | Target Type | Notes |
|---|---|---|---|
| memer_id | string | int, not null | fix column name → member_id |
| full_name | string | string | ✓ |
| EMAIL | string | string | fix column name → email |
| phone | string | string | ✓ |
| address | string | string | ✓ |
| city | string | string | trim whitespace from column name |
| state | string | string | trim whitespace from column name |
| posttcode | string | string | fix column name → postcode |
| date_of_birth | string | date | trim whitespace from column name, standardise format |
| membership_date | string | date | standardise format |
| memebrship_status | string | string | fix column name → membership_status, standardise values |

### Books
| Column | Current Type | Target Type | Notes |
|---|---|---|---|
| book_id | string | int | ✓ |
| title | string | string | ✓ |
| author | string | string | ✓ |
| isbn | string | string | unique, not null |
| genre | string | string | ✓ |
| publisher | string | string | ✓ |
| year_published | string | int | ✓ |
| total_copies | string | int | ✓ |

### Loans
| Column | Current Type | Target Type | Notes |
|---|---|---|---|
| loan_id | string | int, not null | ✓ |
| member_id | string | int | ✓ |
| BOOK_ID | string | int | fix column name → book_id |
| loan_date | string | date | ✓ |
| dueDATE | string | date | fix column name → due_date |
| return_date | string | date | ✓ |
| is_late | string | boolean | standardise values |
| staff_id | string | int | ✓ |

### Staff
| Column | Current Type | Target Type | Notes |
|---|---|---|---|
| staff_id | string | int, not null | ✓ |
| full_name | string | string | ✓ |
| branch | string | string | ✓ |
| role | string | string | ✓ |
| hire_date | string | date | ✓ |

---

## Column Integrity Standards

- **Date format** — all date columns will be standardised to `YYYY-MM-DD`
- **Phone format** — all numbers will be standardised to `04XXXXXXXX` (10 digits, no spaces or special characters)
- **Missing values** — rows will not be dropped unless the missing value invalidates the row entirely. Non-critical nulls will be replaced with `0` or `Unknown` depending on column logic
- **Hidden unknowns** — because multiple representations of the same value exist across columns (e.g. `"0"`, `"Unknown"`, `"N"`), a second pass will be performed after standardisation to confirm no invalid values remain disguised as valid ones. This is particularly relevant for `membership_status` and `is_late`
- **Missing member info** - memebers are not forced to provide any personal information beyond full name and full address , meaning nulls in columns such as email or phone number are simply to be treated as unkown

---

## Dataset Findings

### Members (515 rows)

**member_id**
No missing values. All good.

**full_name**
515 total values, 512 distinct — 3 duplicate members present

**email**
90 out of 515 values missing. Of the 425 present, only 411 are distinct — 14 non-unique emails. Missing values are acceptable as email is not a required field.

**phone**
50 missing values. 451 present, of which only 451 are distinct — some non-unique numbers exist. Numbers appear in multiple formats: standard `04XXXXXXXX`, `+61` prefix, `(04)` prefix, and values with hyphens or spaces. All numbers will be standardised to `04XXXXXXXX`. Each number will also be validated for digit count — exactly 10 digits required.

**address**
No issues. All good.

**city, state**
No data quality issues. Column names contain leading whitespace — will be trimmed.

**postcode**
No issues beyond the column name typo (`posttcode`).

**date_of_birth, membership_date**
Dates appear in multiple formats across rows. All will be standardised to `YYYY-MM-DD`.

**membership_status**
No missing values. 14 distinct values representing only 3 valid states. Mapping required:

| Raw values | Standardised value |
|---|---|
| Active, active, ACTIVE, Yes, Y, 1 | Active |
| Inactive, inactive, No, N, 0 | Inactive |
| Expired, expired, EXP | Expired |

A post standardisation check will confirm no values fall outside these three categories.

---

### Books (515 rows)

**book_id**
No missing values. All good.

**title**
No nulls, all values distinct. All good.

**author**
497 distinct values out of 515 — expected, as one author can publish multiple books. No nulls apparent.

**isbn**
**Issue identified.** ISBN must be unique by definition. The dataset contains 515 rows but only 500 distinct ISBNs — 15 duplicates present. The profiling report did not flag duplicates directly, but the row count vs distinct count confirms they exist. Deduplication will be performed on ISBN specifically, not just row equality.

**genre**
12 distinct values, no nulls. All good.

**publisher**
No issues. All good.

**year_published**
No nulls. Min and max values are within expected range — no impossible dates. 31 distinct values. All good.

**total_copies**
45 out of 500 missing values. Min 4, max 20 across present values. Missing values will be filled with `0` — the decision is that missing inventory means not currently in stock, so `0` is more accurate than null which would imply unknown.

---

### Loans (120 rows)

**loan_id, member_id, book_id**
No issues. All good.

**loan_date, due_date, return_date**
No issues. All good.

**is_late**
No missing values. Multiple representations of true and false present:

| Raw values | Standardised value |
|---|---|
| Yes, YES, True, 1, y | True |
| No, NO, False, 0, N | False |

Will be standardised to boolean.

**staff_id**
No issues. All good.

---

### Staff (18 rows)

**staff_id, full_name**
No issues. All good.

**branch**
3 distinct values: Melbourne, Sydney, Brisbane — all correctly spelled. All good.

**role**
4 distinct values: Analyst, Technician, Support, Manager. All good.

**hire_date**
No issues. All good.
