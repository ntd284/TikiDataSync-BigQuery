import subprocess
from google.cloud import bigquery
import json
def GCS_to_Bigquery():

    print("Local data to Bigquery")

    credentials_path = './credentials.json'

    # Authenticate the BigQuery client
    bq_client = bigquery.Client.from_service_account_json(credentials_path)

    # Define the BigQuery dataset and table details
    dataset_id = 'Tiki_db'
    table_id = 'Tiki_table'

    # Load the JSON data into BigQuery
    dataset_ref = bq_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    # bq_client.create_dataset(dataset_ref, exists_ok=True)

    job_config = bigquery.LoadJobConfig(
    source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    autodetect = True,  # Enable schema auto-detection
    max_bad_records = 50000,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        # Specify the format of the error rows to be recorded
    )

    # Set the GCS URI for the file to be loaded
    gcs_uri = 'gs://project5-backup/Tiki_db.json'
    # Create the load job to load the JSON data into the table
    load_job = bq_client.load_table_from_uri(gcs_uri,location="US", destination=table_ref, job_config=job_config)
    load_job.result()   
    # Wait for the job to complete
    print(f"Loaded {load_job.output_rows} rows into {dataset_id}.{table_id}.")
        
    # Check if there are any errors during the data loading
    if load_job.errors:
        print("Data loaded to BigQuery table with errors:")
        for error in load_job.errors:
            print(error)
            if "json" in error:
                print("Error Row:")
                print(json.dumps(error["json"], indent=2))  # Print the JSON data of the error row
                print("-" * 50)  # Separator between error rows
            else:
                print("Error Row does not contain JSON data.")
    else:
        print("Data loaded to BigQuery table successfully!")

if __name__ == "__main__":
    # Step 3: Load data into BigQuery
    GCS_to_Bigquery()