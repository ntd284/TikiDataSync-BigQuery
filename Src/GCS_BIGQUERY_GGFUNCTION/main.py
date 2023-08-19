from google.cloud import bigquery
from google.cloud import storage

def hello_gcs(event, context):
    print("Cloud Function triggered on GCS event.")
    # Extract the bucket and file name from the event data
    bucket_name = event['bucket']
    file_name = event['name']
    print(f"Bucket: {bucket_name}, File: {file_name}")

    # Authenticate BigQuery and GCS clients
    bq_client = bigquery.Client()
    gcs_client = storage.Client()

    # Define the BigQuery dataset and table details
    dataset_id = 'Tiki_db'
    table_id = 'Tiki_table'

    # Load the JSON data into BigQuery
    dataset_ref = bq_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,  # Enable schema auto-detection
        max_bad_records=50000,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    # Set the GCS URI for the file to be loaded
    gcs_uri = f'gs://{bucket_name}/{file_name}'
    # Create the load job to load the JSON data into the table
    load_job = bq_client.load_table_from_uri(gcs_uri, location="US", destination=table_ref, job_config=job_config)
    load_job.result()

    # Wait for the job to complete
    print(f"Loaded {load_job.output_rows} rows into {dataset_id}.{table_id}.")

    # Check if there are any errors during the data loading
    if load_job.errors:
        print("Data loaded to BigQuery table with errors:")
        for error in load_job.errors:
            print(error)
    else:
        print("Data loaded to BigQuery table successfully!")

if __name__ == "__main__":
    # This block is only for local testing and not required for the Cloud Function deployment.
    event = {
        "bucket": "project5-backup",
        "name": "Tiki_db.json"
    }
    hello_gcs(event, None)
