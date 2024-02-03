import functions_framework
import pandas as pd
from google.cloud import storage, bigquery
import datetime
import pandas_gbq

def read_csv_files(bucket_name, name, project_id, dataset_id, table_id):
    """Reads all CSV files in a Cloud Storage bucket folder, returns a list of DataFrames, and loads the data into a BigQuery table."""
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(name)
    blob.download_to_filename(name)
        
    # Create a BigQuery client
    bq_client = bigquery.Client(project=project_id)
    
    # for blob in blobs:
    if name.endswith("test"):
        try:
            dataframe = pd.read_csv(name)
            # Calculate registration date
            dataframe["DATE_REGISTRATION"] = pd.to_datetime(dataframe["DAYS_REGISTRATION"], unit='D')

            # Extract year, month, and day from the registration date
            dataframe["YEAR_REGISTRATION"] = dataframe["DATE_REGISTRATION"].dt.year.astype(int)
            dataframe["MONTH_REGISTRATION"] = dataframe["DATE_REGISTRATION"].dt.month.astype(int)
            dataframe["DAY_REGISTRATION"] = dataframe["DATE_REGISTRATION"].dt.day.astype(int)

            # Calculate DAYS_LAST_PHONE_CHANGE_FIXED
            dataframe["DAYS_LAST_PHONE_CHANGE_FIXED"] = dataframe["DAYS_LAST_PHONE_CHANGE"] / -360

            # Round the column to 0 decimal places
            dataframe["DAYS_LAST_PHONE_CHANGE_FIXED"] = dataframe["DAYS_LAST_PHONE_CHANGE_FIXED"].round(0)

            # Replace -0.0 with 0.0
            dataframe["DAYS_LAST_PHONE_CHANGE_FIXED"] = dataframe["DAYS_LAST_PHONE_CHANGE_FIXED"].replace(-0.0, 0.0)

            # Define function for categorizing phone change
            def days_last_phone_change(phone):
                if phone == 0:
                    return 'Never'
                elif 1 <= phone <= 3:
                    return 'Ever'
                else:
                    return 'Frequent'

            # Apply function to create PHONE_CHANGE_CAT column
            dataframe["PHONE_CHANGE_CAT"] = dataframe["DAYS_LAST_PHONE_CHANGE_FIXED"].apply(days_last_phone_change)
            
            # Define Age from Days Births
            dataframe['AGE'] = dataframe['DAYS_BIRTH']/-360
            decimals = 0
            dataframe['AGE'] = dataframe['AGE'].apply(lambda x: round(x, decimals))
            
            # Categorize Age
            def age_category(age):
                if age < 20:
                    return 'Late Ten'
                elif age >= 20 and age < 30:
                    return 'Twenty'
                elif age >= 30 and age < 40:
                    return 'Thirty'
                elif age >= 40 and age < 50:
                    return 'Fourty'
                elif age >= 50 and age < 60:
                    return 'Fifty'
                else:
                    return 'Above Sixty'

            dataframe['AGE_CATEGORY'] = dataframe['AGE'].apply(age_category)
            
            # Categorize Income
            def income_category(income):
                if income < 112500:
                    return 'Low Income'
                elif income >= 112500 and income < 202500:
                    return 'Mid Income'
                else:
                    return 'High Income'

            dataframe['AMT_INCOME_CAT'] = dataframe['AMT_INCOME_TOTAL'].apply(income_category)
            
            # Change code gender F (Female) and M (Male)
            def map_gender(value):
                if value == 'F':
                    return 'Female'
                elif value == 'M':
                    return 'Male'
                else:
                    return 'Unrecognized'

            # Apply the function to the 'CODE_GENDER' column
            dataframe['CODE_GENDER'] = dataframe['CODE_GENDER'].apply(map_gender)


        except pd.errors.ParserError:
            print(f"Error parsing CSV file: {name}")
    
    print('a', dataframe)
    
    pandas_gbq.to_gbq(dataframe, table_id, project_id=project_id, if_exists='append')

    return dataframe

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def hello_gcs(cloud_event):
    data = cloud_event.data
    print('data=', data)
    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    name = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")

    bucket_name = data["bucket"]
    project_id = "corporate-digital"
    dataset_id = "CREDIVO_DW"
    table_id = "corporate-digital.CREDIVO_DW.application_test_clean"
    
    dataframe = read_csv_files(bucket_name, name, project_id, dataset_id, table_id)
    pandas_gbq.to_gbq(dataframe, table_id, project_id, if_exists='append')

    print(dataframe.head())