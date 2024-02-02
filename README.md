# **Credivo Data Pipeline**

## Project Overview:
Credivo, a cutting-edge company, grapples with a wealth of data from diverse sources, presenting an opportunity for informed decision-making and valuable insights. However, the challenge lies in the effective utilization of this data and the prevalent issue of inadequate Data Quality. Compounding the problem, stakeholders lack access to tools that allow them to assess and ensure the reliability of the data.

Recognizing the need for a transformative solution, Credivo is poised to implement an advanced data pipeline. This pipeline aims to streamline data organization, enhancing accessibility and instilling trust in the information. The primary goal is to empower the Credivo team with timely and accurate data, enabling them to make informed decisions that contribute to the company's overall improvement.

## Pipeline:
![image](https://github.com/ariqarfina/credivo_pipeline/assets/101324931/e6228cbe-d66f-45b4-8892-d7c46dd6f682)


**Requirements & Components**
1. Docker Compose Configuration:
   - **File:** `docker-compose-airflow.yml`, `docker-compose-postgres.yml`
   - **Services:**
      - `Airflow Scheduler`
      - `Airflow Webserver`
      - `Postgres`
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
   - **File:** `Dockerfile.airflow-arm
5. Makefile:
   - **File:** `Makefile`
   - **Commands:**
      - `run-all`: Starts all the containers (`Airflow` and `Posgres`)
      - `stop-all`: Stops all the containers (`Airflow` and `Posgres`).
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
      - Create and define data profile name as `DP - CRDV APPLICATION TEST`
      - Set profiling scope to Entire Data
      - Send the profile test to BigQuery Dataset named  `CREDIVO_DW` and name it as `DP_{Table_Name}` (In this case, we use `application_test` data to run the whole process

Output:
- Automated pipeline (daily) to load data from MySQL Database to GCS (Raw Data) and BigQuery (Raw Data) and Create Data Profile Job in Dataplex
- Running cloud function (python operator) to transform data and load data to BigQuery (Transformed Data)
- Dashboard for Data Quality and Credit Data Insight


Data Quality Dashboard:
<img width="783" alt="Screenshot 2024-02-02 at 14 02 53" src="https://github.com/ariqarfina/credivo_pipeline/assets/101324931/c91ca8ec-2fab-4b88-8ec3-ba4d657fd401">













#### Final Project of Data Engineering at Dibimbing Bootcamp
