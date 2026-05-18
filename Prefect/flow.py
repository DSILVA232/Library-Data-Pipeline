from prefect import flow, task, get_run_logger
from pathlib import Path
import subprocess
import snowflake.connector
import os
from dotenv import load_dotenv

# setup
load_dotenv(Path(__file__).parent.parent / ".env")

DBT_PROJECT_DIR = str(Path(__file__).parent.parent / "dbt" / "library_project")
SPARK_DIR = str(Path(__file__).parent.parent / "spark")

ingestion_sql = (Path(__file__).parent.parent / "SQL" / "ingestion.sql").read_text()
ingestion_statements = [s.strip() for s in ingestion_sql.split(";") if s.strip()]


@task(retries=2, retry_delay_seconds=10)
def run_spark():
    logger = get_run_logger()
    logger.info("starting spark cleaning job via docker")
    subprocess.run(["docker-compose","up","--build","--abort-on-container-exit"],cwd =str(Path(__file__).parent.parent) , check=True)
    logger.info("spark cleaning complete")


@task(retries=2, retry_delay_seconds=10)
def run_s3_upload():
    logger = get_run_logger()
    logger.info("uploading parquet files to S3")
    subprocess.run(["python3", f"{SPARK_DIR}/s3_upload.py"], check=True)
    logger.info("S3 upload complete")


@task(retries=2, retry_delay_seconds=10)
def run_snowflake_ingestion():
    logger = get_run_logger()
    conn = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema="RAW"
    )
    cursor = conn.cursor()
    logger.info("running COPY INTO statements")
    for statement in ingestion_statements:
        cursor.execute(statement)
    conn.close()
    logger.info("snowflake ingestion complete")


@task(retries=2, retry_delay_seconds=10)
def run_dbt_snapshot():
    logger = get_run_logger()
    logger.info("installing dbt packages")
    subprocess.run(["dbt", "deps", "--project-dir", DBT_PROJECT_DIR], check=True)
    logger.info("running dbt snapshot")
    subprocess.run(["dbt", "snapshot", "--project-dir", DBT_PROJECT_DIR], check=True)
    logger.info("dbt snapshot complete")


@task(retries=2, retry_delay_seconds=10)
def run_dbt_models():
    logger = get_run_logger()
    logger.info("running dbt models")
    subprocess.run(["dbt", "run", "--project-dir", DBT_PROJECT_DIR], check=True)
    logger.info("dbt models complete")


@task(retries=2, retry_delay_seconds=10)
def run_dbt_tests():
    logger = get_run_logger()
    logger.info("running dbt tests")
    subprocess.run(["dbt", "test", "--project-dir", DBT_PROJECT_DIR], check=True)
    logger.info("dbt tests complete")


@flow(name="library-pipeline")
def library_pipeline():
    run_spark()
    run_s3_upload()
    run_snowflake_ingestion()
    run_dbt_snapshot()
    run_dbt_models()
    run_dbt_tests()


if __name__ == "__main__":
    library_pipeline()