import boto3
import os
from pathlib import Path
from dotenv import load_dotenv

#set up
load_dotenv(Path(__file__).parent.parent / ".env")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
)

local_output = Path(__file__).parent.parent / "spark" / "output"
bucket_name = os.getenv("AWS_BUCKET_NAME")


#function

def upload_folder(local_folder, s3_prefix):
    for file in local_folder.rglob("*"):
        if file.is_file():
            s3_key = f"{s3_prefix}/{file.relative_to(local_folder)}"
            s3.upload_file(str(file), bucket_name, s3_key)
            print(f"uploaded: {s3_key}")



#call
upload_folder(local_output / "members", "raw/members")
upload_folder(local_output / "staff",   "raw/staff")
upload_folder(local_output / "books",   "raw/books")
upload_folder(local_output / "loans",   "raw/loans")


#check
print("all files uploaded to S3")