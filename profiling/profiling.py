import pandas as pd 
import sweetviz as sv
from pathlib import Path


path = Path(__file__).parent.parent / "data" 

members_df = pd.read_csv(str(path / "members.csv"))
books_df   = pd.read_csv(str(path / "books.csv"))
loans_df   = pd.read_csv(str(path / "loans.csv"))
staff_df   = pd.read_csv(str(path / "staff.csv"))


output_path = Path(__file__).parent / "reports"
output_path.mkdir(exist_ok=True)

sv.analyze(members_df).show_html(str(output_path / "members_report.html"),open_browser=False)
sv.analyze(books_df).show_html(str(output_path / "books_report.html"),open_browser=False)
sv.analyze(loans_df).show_html(str(output_path / "loans_report.html"),open_browser=False)
sv.analyze(staff_df).show_html(str(output_path / "staff_report.html"),open_browser=False)

print("Reports generated successfully,check reports folder.")