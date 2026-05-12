import pandas as pd 
import sweetviz as sv
from pathlib import Path


path = Path(__file__).parent.parent / "data_raw" 

members_df = pd.read_csv(str(path / "members.csv"))
books_df   = pd.read_csv(str(path / "books.csv"))
loans_df   = pd.read_csv(str(path / "loans.csv"))
staff_df   = pd.read_csv(str(path / "staff.csv"))




# auto report bulding (uncoment and run once)
output_path = Path(__file__).parent / "reports"
output_path.mkdir(exist_ok=True)

sv.analyze(members_df).show_html(str(output_path / "members_report.html"),open_browser=False)
sv.analyze(books_df).show_html(str(output_path / "books_report.html"),open_browser=False)
sv.analyze(loans_df).show_html(str(output_path / "loans_report.html"),open_browser=False)
sv.analyze(staff_df).show_html(str(output_path / "staff_report.html"),open_browser=False)

print("Reports generated successfully,check reports folder.")


# Further manual profiling is conducted here to investigate possible unknown/null values hiding as strings.
# A reusable function handles both checks across all tables:
#   1. Known null representations (e.g. "none", "na", "0", "-") matched via an explicit list
#   2. Suspiciously short string values that may indicate placeholder data
# Note: some columns contain legitimate values that overlap with null representations (e.g. "0" in numeric columns).
# Results should be interpreted with column context in mind before labelling a column as dirty.



def check_nulls(df, name, suspicious_cols, null_representations, length_cols=None, length_threshold=5):
    print(f"\n{'='*40}")
    print(f"TABLE: {name}")
    print(f"{'='*40}")
    
    # check for hidden null representations
    if suspicious_cols:
        mask = df[suspicious_cols].apply(lambda col: col.astype(str).str.strip().str.lower().isin(null_representations))

        matches = df[mask.any(axis=1)]
        print(f"\nSuspected nulls in {suspicious_cols}:")
        print(f"  {len(matches)} rows found")
        if len(matches) > 0:
            print(matches[suspicious_cols])

    # check for suspiciously short strings
    if length_cols:
        for col in length_cols:
            short = df[df[col].astype(str).str.len() < length_threshold]

            print(f"\nShort values in '{col}' (< {length_threshold} chars):")
            print(f"  {len(short)} rows found")
            if len(short) > 0:
                print(short[[col]])


null_representations = ["", " ", "null", "none", "na", "n/a", "unknown", "-", "?", "0"]

check_nulls(members_df, "members",
    suspicious_cols=["memer_id", "phone", "EMAIL"],
    null_representations=null_representations,
    length_cols=["full_name", "EMAIL", "phone"]
)

check_nulls(books_df, "books",
    suspicious_cols=["book_id", "isbn", "total_copies"],
    null_representations=null_representations,
    length_cols=["author", "title"]
)

check_nulls(loans_df, "loans",
    suspicious_cols=["loan_id", "member_id", "BOOK_ID", "is_late"],
    null_representations=null_representations
)

check_nulls(staff_df, "staff",
    suspicious_cols=["staff_id", "branch", "role"],
    null_representations=null_representations,
    length_cols=["full_name"]
)