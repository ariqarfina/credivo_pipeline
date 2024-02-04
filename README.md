# **Credivo Data Pipeline**

## Project Overview:
Credivo, like many modern companies, deals with a lot of data from different sources. This data can help make smart decisions and find important insights, but it's hard to use effectively.

To fix this, Credivo knows it needs a better data pipeline for managing data. This pipeline will organize the data better, making it easier to use and trust. With this pipeline, Credivo wants to give its team the right information at the right time, so they can make better decisions and make the company better overall.

## Pipeline:
![image](https://github.com/ariqarfina/credivo_pipeline/assets/101324931/e6228cbe-d66f-45b4-8892-d7c46dd6f682)


**Requirements & Components**
1. Docker Compose Configuration:
   - **File:** `docker-compose-airflow.yml`, `docker-compose-postgres.yml`, `docker-compose-jupyter.yml`
   - **Services:**
      - `Airflow Scheduler` : for scheduling in airflow
      - `Airflow Webserver` : for Airflow UI
      - `Postgres` : for Airflow database (Staging database, save temporary file while airflow is processing)
      - `Jupyter` : for developing code
2. Airflow DAG (Directed Acyclic Graph):
   - **File:** `[run]credivo-dag-gcs.py`
   - **Description:**
      - Define an Airflow DAG named `move_mysql_to_gbg` for loading raw data from MySQL to Google Cloud Storage (Raw Data) and BigQuery (Raw Data)
      - Import Variable and define variable in DAG file such as `BUCKET_NAME`, `SQL_QUERY`, `FILENAME`, `GCP_CONN_ID`, `MYSQL_CONN_ID`, and `DESTINATION_DATASET_TABLE`
      - Use `MySQLToGCSOperator` to load raw data from MySQL to Google Cloud Storage
      - Use `GCSToBigQueryOperator` to load raw data from Google Cloud Storage to BigQuery
      - Schedules the DAG to run daily and set dependecies
3. Environment:
   -  **File:** `.Env`
4. Dockerfile:
   - **File:** `Dockerfile.airflow-arm`, `Dockerfile.jupyter` (text document containing all the commands the user requires to call on the command line to assemble an image)
5. Makefile:
   - **File:** `Makefile`
   - **Commands:**
      - `run-all`: Starts all the containers (`Airflow`, `Posgres`, and `Jupyter`)
      - `stop-all`: Stops all the containers (`Airflow`, `Posgres`, and `Jupyter`).
6. Google Cloud Bucket
   - **Description:**
      - Create and define bucket name as `crdivo_lake`
      - Location type : Region
      - Location : asia-southeast2 (Jakarta)
      - Storage Class : Standard (We consider to use standard because of the usage activity is actively used)
7. BigQuery Dataset
   - **Description:**
      - Create New dataset and define name as `CREDIVO_DW` to store Raw Data and Transformed Data
      - Data location : asia-southeast2 (Jakarta)
8. Cloud Function
   - **Description:**
     - Create new function named `credivo_transform` to transform data that stored in Google Cloud Storage to BigQuery
     - Region : asia-southeast2
     - Memory allocated : 2 GiB
     - CPU : 1
     - Timeout : 60 seconds
     - Minimum instances : 0
     - Maximum instances: 100  
9. Service Account for Credentials
   - **Description:**
      - Create and define service account name as `local-airflow-mysql-gcs` to generate google cloud credential key
10. Data Profiling Scan on Google Cloud Dataplex:
      - **Description:**
         - Create and define data profile name as `DP - CRDV APPLICATION TEST PROFILE`
         - Set profiling scope to Entire Data
         - Send the profile test to BigQuery Dataset named  `CREDIVO_DW` and name it as `DP_{Table_Name}` (In this case, we use `application_test` data to run the whole process

Output:
- Automated pipeline (daily) to load data from MySQL Database to GCS (Raw Data) and BigQuery (Raw Data) and Create Data Profile Job in Dataplex
- Running cloud function (python operator) to transform data and load data to BigQuery (Transformed Data)
- Dashboard for Data Quality and Credit Data Insight


Dashboard:

<img width="690" alt="Screenshot 2024-02-03 at 12 47 35" src="https://github.com/ariqarfina/credivo_pipeline/assets/101324931/8d3e13fe-1cde-495f-af8b-9bd0a88e60f0">
<img width="689" alt="Screenshot 2024-02-03 at 12 49 04" src="https://github.com/ariqarfina/credivo_pipeline/assets/101324931/e412f96a-c8ef-403b-bc20-320b83c0def9">

https://lookerstudio.google.com/reporting/b1ed1241-facb-43ba-a7e2-090010207b3f











#### Final Project of Data Engineering at Dibimbing Bootcamp
