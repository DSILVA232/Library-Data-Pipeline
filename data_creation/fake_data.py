from faker import Faker
import pandas as pd
import random
from random import randint
from datetime import timedelta
from datetime import date
import re
from pathlib import Path


fake = Faker('en_AU')


class fake_member:

    def dirty_phone():
        number = fake.numerify("04########")
        fmt = random.random()
        if fmt < 0.25:
            return f"{number[:4]} {number[4:]}"
        elif fmt < 0.50:
            return f"+61 {number[1:]}"
        elif fmt < 0.75:
            return f"({number[:2]}) {number[2:6]}-{number[6:]}"
        else:
            return number

    def dirty_date(fake_date):
        r = random.random()
        if r < 0.33:
            return fake_date.strftime("%d/%m/%Y")
        elif r < 0.66:
            return fake_date.strftime("%B %d, %Y")
        else:
            return str(fake_date)

    def dirty_status():
        status_map = {
            "Active":   ["Active", "active", "ACTIVE", "Yes", "Y", "1"],
            "Inactive": ["Inactive", "inactive", "No", "N", "0"],
            "Expired":  ["Expired", "expired", "EXP"]
        }
        key = random.choice(list(status_map.keys()))
        return random.choice(status_map[key])

    def generate_fake_member_db():
        fake.unique.clear()  # ✅ clear BEFORE generating
        list_of_ids = [fake.unique.random_int(min=1, max=500) for i in range(500)]
        fake.unique.clear()
        table = []

        for i in range(500):
            member = {}
            full_name = fake.name()
            clean_name = re.sub(r"\s+", ".", full_name.strip())
            email = clean_name.lower() + "@gmail.com"
            member["memer_id"]          = list_of_ids[i]
            member["full_name"]         = full_name
            member["EMAIL"]             = None if random.random() < 0.15 else email
            member["phone"]             = None if random.random() < 0.10 else fake_member.dirty_phone()
            member["address"]           = fake.street_address()
            member[" city"]             = fake.city()
            member[" state"]            = fake.state()
            member["posttcode"]         = fake.postcode()
            member[" date_of_birth"]    = fake_member.dirty_date(fake.date_of_birth(minimum_age=18, maximum_age=65))
            member["membership_date"]   = fake_member.dirty_date(fake.past_date(start_date='-5y'))
            member["memebrship_status"] = fake_member.dirty_status()
            table.append(member)

        df = pd.DataFrame(table)

        duplicates = []
        for _, row in df.sample(frac=0.03, random_state=42).iterrows():
            dupe = row.copy()
            dupe["full_name"] = row["full_name"].upper()
            dupe["memer_id"]  = df["memer_id"].max() + len(duplicates) + 1
            duplicates.append(dupe)

        df = pd.concat([df, pd.DataFrame(duplicates)], ignore_index=True)
        return df


class fake_book:

    def generate_fake_book():
        fake.unique.clear()  # ✅ clear BEFORE generating
        list_of_genres = [
            "Fantasy", "Science Fiction", "Mystery", "Thriller", "Romance",
            "Historical Fiction", "Horror", "Biography", "Self-Help",
            "Business", "Psychology", "Young Adult"
        ]
        list_of_ids        = [fake.unique.random_int(min=1, max=500) for i in range(500)]
        fake.unique.clear()
        list_of_publishers = [fake.unique.company() for i in range(23)]
        fake.unique.clear()
        book_table = []

        for i in range(500):
            book = {}
            book["book_id"]        = list_of_ids[i]
            book["title"]          = fake.catch_phrase()
            book["author"]         = fake.name()
            book["isbn"]           = fake.isbn13()
            book["genre"]          = random.choice(list_of_genres)
            book["publisher"]      = random.choice(list_of_publishers)
            book["year_published"] = fake.date_between(start_date='-30y', end_date='today').year
            book["total_copies"]   = None if random.random() < 0.10 else fake.random_int(min=4, max=20)
            book_table.append(book)

        df = pd.DataFrame(book_table)

        duplicates = []
        for _, row in df.sample(frac=0.03, random_state=42).iterrows():
            dupe = row.copy()
            dupe["title"]   = row["title"].upper()
            dupe["book_id"] = df["book_id"].max() + len(duplicates) + 1
            duplicates.append(dupe)

        df = pd.concat([df, pd.DataFrame(duplicates)], ignore_index=True)
        fake.unique.clear()
        return df


class loans:

    def generate_loan():
        fake.unique.clear()  # ✅ clear BEFORE generating
        list_of_member_ids = [fake.unique.random_int(min=1, max=500) for i in range(120)]
        fake.unique.clear()
        list_of_book_ids   = [fake.unique.random_int(min=1, max=500) for i in range(120)]
        fake.unique.clear()
        list_of_loan_ids   = [fake.unique.random_int(min=1, max=120) for i in range(120)]
        fake.unique.clear()
        late_options = ["Yes", "YES", "True", "1", "y"]
        no_options   = ["No", "NO", "False", "0", "N"]
        loan_table   = []

        for i in range(120):
            loan = {}
            loan_date   = fake.date_between(start_date='-1y', end_date='today')
            due_date    = loan_date + timedelta(days=30)
            return_date = loan_date + timedelta(days=randint(1, 90))

            loan["loan_id"]     = list_of_loan_ids[i]
            loan["member_id"]   = list_of_member_ids[i]
            loan["BOOK_ID"]     = list_of_book_ids[i]
            loan["loan_date"]   = loan_date
            loan["dueDATE"]     = due_date
            loan["return_date"] = return_date
            loan["late_fee"]    = random.choice(late_options) if return_date > due_date else random.choice(no_options)
            loan_table.append(loan)

        df = pd.DataFrame(loan_table)
        fake.unique.clear()
        return df


class staff:

    def generate_staff():
        fake.unique.clear() \


        
        list_of_staff_ids = [fake.unique.random_int(min=1, max=18) for i in range(18)]
        fake.unique.clear()
        staff_table = []
        branches = ["Sydney", "Melbourne", "Brisbane"]
        roles    = ["Manager", "Analyst", "Support", "Technician"]

        for i in range(18):
            staff_member = {}
            staff_member["staff_id"]  = list_of_staff_ids[i]
            staff_member["full_name"] = fake.name()
            staff_member["branch"]    = random.choice(branches)
            staff_member["role"]      = random.choice(roles)
            staff_member["hire_date"] = fake.date_between(start_date=date(2015, 1, 1), end_date=date(2025, 12, 31))
            staff_table.append(staff_member)

        df = pd.DataFrame(staff_table)
        fake.unique.clear()
        return df


members_df = fake_member.generate_fake_member_db()
book_df    = fake_book.generate_fake_book()
loans_df   = loans.generate_loan()
staff_df   = staff.generate_staff()

output_path = Path(__file__).parent.parent / "data"
output_path.mkdir(exist_ok=True)  

members_df.to_csv(output_path / "members.csv", index=False)  
book_df.to_csv(output_path / "books.csv", index=False)        
loans_df.to_csv(output_path / "loans.csv", index=False)
staff_df.to_csv(output_path / "staff.csv", index=False)

print("Data generated and saved successfully.")