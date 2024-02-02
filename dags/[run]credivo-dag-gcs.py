from airflow import DAG
from datetime import datetime, date, timedelta
import os
from airflow.providers.google.cloud.transfers.mysql_to_gcs import MySQLToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.models import Variable

#dag arguments
default_args = {
    'owner': 'ariq',
    'start_date': datetime(2022, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

#define dag
dag = DAG('move_mysql_to_gbg',
          schedule_interval= None,
          default_args= default_args,
          description="Moving Data from MySQL to BigQuery",
          dagrun_timeout=timedelta(minutes=60)
          )

BUCKET_NAME = Variable.get("bucket_name")
SQL_QUERY = Variable.get("simple_query_all")
FILENAME = Variable.get("gcs_file")
GCP_CONN_ID = Variable.get("gcp_conn_id")
MYSQL_CONN_ID = Variable.get("mysql_conn_id")
DESTINATION_DATASET_TABLE = Variable.get("destination_dataset_table")

# Upload MySQL to GCS (Raw)
upload_mysql_to_gcs = MySQLToGCSOperator(
        task_id="mysql_to_gcs", 
        mysql_conn_id=MYSQL_CONN_ID,
        sql=SQL_QUERY, 
        bucket=BUCKET_NAME, 
        gcp_conn_id  = GCP_CONN_ID,
        filename=FILENAME, 
        export_format="csv",
        dag=dag
    )

# Upload GCS to GBQ (Raw)
gcs_to_gbq = GCSToBigQueryOperator(
        task_id="gcs_to_gbq", 
        bucket=BUCKET_NAME, 
        gcp_conn_id  = GCP_CONN_ID,
        source_objects=[FILENAME], 
        source_format="CSV",
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_TRUNCATE",
        destination_project_dataset_table=DESTINATION_DATASET_TABLE,
        dag=dag
    )

#Define task pipeline
upload_mysql_to_gcs>> gcs_to_gbq