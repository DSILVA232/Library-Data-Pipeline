import boto3
import os
from pathlib import Path



local_output = Path("/app/spark_output")
bucket_name = os.getenv("AWS_BUCKET_NAME")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
)

#delete bucket contents function( note this function has a 1000 objects delete limitation)
def clear_s3_prefix(prefix,bucket = bucket_name):
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

    if "Contents" in response:
        objects_to_delete = [{"Key": obj["Key"]} for obj in response["Contents"]]

        s3.delete_objects(
            Bucket=bucket,
            Delete={"Objects": objects_to_delete}
        )

        print(f"deleted existing files in {prefix}")

# upload files to bucket function

def upload_folder(local_folder, s3_prefix,bucket_name):

    #this clears the data in the bucket (check upload note in README)
    clear_s3_prefix(s3_prefix,bucket_name)

    for file in local_folder.rglob("*"):
        if file.is_file():
            s3_key = f"{s3_prefix}/{file.relative_to(local_folder)}"
            s3.upload_file(str(file), bucket_name, s3_key)
            print(f"uploaded: {s3_key}")



#call
upload_folder(local_output / "members", "raw/members",bucket_name)
upload_folder(local_output / "staff",   "raw/staff",bucket_name)
upload_folder(local_output / "books",   "raw/books",bucket_name)
upload_folder(local_output / "loans",   "raw/loans",bucket_name)


#check
print("all files uploaded to S3")