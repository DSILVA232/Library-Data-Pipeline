from pyspark.sql import SparkSession
from pathlib import Path
from pyspark.sql.functions import try_to_date, coalesce, col, regexp_replace, when, length, lower, trim, count


# PySpark cleaning job — structural data cleaning only, no business logic.
# All cleaning steps were identified during the profiling phase and are documented in the profiling report.
# Goal: produce clean, consistently typed, consistently formatted data ready for S3 ingestion.


# ── paths & session ───────────────────────────────────────────────────────────

path = Path(__file__).parent.parent / "data_raw"
output_path = Path(__file__).parent / "output" 
output_path.mkdir(exist_ok=True)

spark = SparkSession.builder \
    .appName("library-pipeline") \
    .master("local[*]") \
    .getOrCreate()


# ── lookup tables ─────────────────────────────────────────────────────────────

active_values      = ["active", "yes", "y", "1"]
inactive_values    = ["inactive", "no", "n", "0"]
expired_values     = ["expired", "exp"]

is_late_yes_values = ["yes", "true", "1", "y"]
is_late_no_values  = ["no", "false", "0", "n"]


# ── shared functions ──────────────────────────────────────────────────────────

def clean_column_name(name):
    return name.strip().lower().replace(" ", "_").replace(".", "_")


def standardise_date(column_name):
    return coalesce(
        try_to_date(col(column_name), "yyyy-MM-dd"),
        try_to_date(col(column_name), "dd/MM/yyyy"),
        try_to_date(col(column_name), "MM/dd/yyyy"),
        try_to_date(col(column_name), "MMMM dd, yyyy"),
        try_to_date(col(column_name), "MMM dd, yyyy"),
        try_to_date(col(column_name), "dd-MM-yyyy"),
        try_to_date(col(column_name), "yyyy/MM/dd"),
    )


def standardise_phone(column_name):
    stripped = regexp_replace(col(column_name), r"[^\d]", "")
    return (
        when(col(column_name).isNull(), None)
        .when(stripped.startswith("61"), regexp_replace(stripped, "^61", "0"))
        .otherwise(stripped)
    )


def standardise_status(column_name):
    cleaned = lower(trim(col(column_name)))
    return (
        when(cleaned.isin(active_values),   "Active")
        .when(cleaned.isin(inactive_values), "Inactive")
        .when(cleaned.isin(expired_values),  "Expired")
        .otherwise(None)
    )


def standardise_is_late(column_name):
    cleaned = lower(trim(col(column_name)))
    return (
        when(cleaned.isin(is_late_yes_values), True)
        .when(cleaned.isin(is_late_no_values),  False)
        .otherwise(None)
    )


# ── members ───────────────────────────────────────────────────────────────────

members_df = spark.read.csv(str(path / "members.csv"), header=True)

# column names
members_df = members_df.toDF(*[clean_column_name(c) for c in members_df.columns])
members_df = members_df.withColumnsRenamed({
    "memer_id":          "member_id",
    "posttcode":         "postcode",
    "memebrship_status": "membership_status",
})

# dates
members_df = members_df.withColumn("date_of_birth",   standardise_date("date_of_birth"))
members_df = members_df.withColumn("membership_date", standardise_date("membership_date"))

# phone — strip non-digits, normalise +61 prefix, enforce 10 digits
members_df = members_df.withColumn("phone", standardise_phone("phone"))
members_df = members_df.withColumn("phone", when(length(col("phone")) == 10, col("phone")).otherwise(None))

# membership status
members_df = members_df.withColumn("membership_status", standardise_status("membership_status"))

# deduplication — member_ids were grouped and counted beforehand to confirm no id collisions
members_df = members_df.dropDuplicates(["member_id"])

# cast types
members_df = members_df.withColumn("member_id", col("member_id").cast("int"))


# ── staff ─────────────────────────────────────────────────────────────────────

staff_df = spark.read.csv(str(path / "staff.csv"), header=True)

# column names
staff_df = staff_df.toDF(*[clean_column_name(c) for c in staff_df.columns])

# dates
staff_df = staff_df.withColumn("hire_date", standardise_date("hire_date"))

# cast types
staff_df = staff_df.withColumn("staff_id", col("staff_id").cast("int"))


# ── books ─────────────────────────────────────────────────────────────────────

books_df = spark.read.csv(str(path / "books.csv"), header=True)

# column names
books_df = books_df.toDF(*[clean_column_name(c) for c in books_df.columns])

# deduplication — isbns were grouped and counted beforehand to confirm no id collisions
# isbn is the natural unique key for books — duplicates are dirty rows not separate editions
books_df = books_df.dropDuplicates(["isbn"])

# cast types first — float intermediate handles values like '14.0' stored as strings
book_cols_to_cast = ["book_id", "year_published", "total_copies"]
books_df = books_df.select([
    col(c).cast("float").cast("int").alias(c) if c in book_cols_to_cast else col(c)
    for c in books_df.columns
])

# fill missing total_copies with 0 — missing inventory means not currently in stock
books_df = books_df.na.fill({"total_copies": 0})


# ── loans ─────────────────────────────────────────────────────────────────────

loans_df = spark.read.csv(str(path / "loans.csv"), header=True)

# column names
loans_df = loans_df.toDF(*[clean_column_name(c) for c in loans_df.columns])
loans_df = loans_df.withColumnsRenamed({"duedate": "due_date"})

# is_late — standardise multiple representations to boolean
loans_df = loans_df.withColumn("is_late", standardise_is_late("is_late"))

# cast types
loan_cols_to_cast = ["loan_id", "member_id", "book_id", "staff_id"]
loans_df = loans_df.select([
    col(c).cast("float").cast("int").alias(c) if c in loan_cols_to_cast else col(c)
    for c in loans_df.columns
])

# dates
loans_df = loans_df.withColumn("loan_date",standardise_date("loan_date"))
loans_df = loans_df.withColumn("due_date",standardise_date("due_date"))
loans_df = loans_df.withColumn("return_date",standardise_date("return_date"))




#write to paraquet file

# overwrite mode used here because this is a full refresh pipeline.
# for incremental data, append mode would be used instead.

members_df.write.mode("overwrite").parquet(str(output_path / "members"))
staff_df.write.mode("overwrite").parquet(str(output_path / "staff"))
books_df.write.mode("overwrite").parquet(str(output_path / "books"))
loans_df.write.mode("overwrite").parquet(str(output_path/ "loans"))