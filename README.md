# Synchronize all Tiki product data to Data Warehouse BigQuery with data from Mongodb.

## A fully functional project written in python to create a basic ETL process with Mongodb, Google cloud storage, Bigquery and Data Studio.

This project was build with the main target of transforming data from non-sequential to sequential using Bigquery and conducting data analysis using SQL. Additionally, this project also integrates automations in daily updating of data to Bigquery using Mongodb on Google virtual machine(VM), Google Cloud Storage(GCS) and Google function. Every part of this project shows how to do the followings:

* Data is fetched from Mongodb will be cleaned, structured at local machine with python.
* Formatted data will be transfered to GCS to backup.
* When google functions detect trigger of updating on GCS, it run available code to transfer all data to bigquery.
* All of process is automatically operate on Virtual machine.
* Data is used to analyze some pratical cases in business by using visualization in dashboard.

## Step by step of this project.

### 0.Setup:

* Install and initialize VM, GCS, Bigquery, Mongodb.
* Install `gsutil` command-line tool (Google Cloud SDK).
* Create API in "credentials.json" format.

### 1. Fetch data from Mongodb and transfer to json format.
[Script: 1.MongoDB_to_JSON_to_GCS.py](./src/MONGODB_GCS_BIGQUERY/1.MongoDB_to_JSON_to_GCS.py)
Parameters: None

* Workflow:
1. Connects to the local Mongodb instance.
2. Fetches documents from the `Tiki` collection.
3. Structured some specific fields to suitable with bigquery format, such as: `_id`,`crawled_time`,`installment_info_v2`, ect. 
4. Exports the cleaned data to JSONL file, which ready for next process in Bigquery.

### 2. Upload Local Data to Google Cloud Storage (GCS).
[Script: 1.MongoDB_to_JSON_to_GCS.py](./src/MONGODB_GCS_BIGQUERY/1.MongoDB_to_JSON_to_GCS.py)
Parameters: None

* Workflow:
1. Specifies the Google Cloud Storage bucket name and desired filename in GCS (`project5-backup` and `Tiki_db.json`, respectively).
2. Uses `gsutil` to upload the local JSONL file to GCS. 
`gsutil -o "GSUtil:parallel_composite_upload_threshold=150M" -m cp /Users/macos/Documents/Python/DEC/DE_PROJECT_5/Data/Tiki_.json gs://project5-backup/Tiki_db.json`
3. Especially, `gsutil` command run with parallel composite upload enabled for faster performance.

### 3. Transfer GCS data to Bigquery.
[Script: 2.GCS_to_Bigquery.py](./src/MONGODB_GCS_BIGQUERY/2.GCS_to_Bigquery.py)
Parameters: None

* Workflow:
1. Authenticates the Bigquery client using `credentials.json`.
2. Defines the BigQuery data set (`Tiki_db`) and table (`Tiki_table`) where the data will be loaded.
3. Configures the load job to use JSON as the source format with schema auto-detection.
4. Specifies the GCS URI of the file (`gs://project5-backup/Tiki_db.json`) to be loaded into the Bigquery table.
5. Load the JSON data into the designated Bigquery table.

### 3.Create a Datamart table for seller and products for Data Analyst.
[Script: BIGQUERY_Datamart.txt](./src/BIGQUERY_Datamart.txt)
Parameters: None

* Selected with `name_product`, `category`, `brand_origin`, `brand`, `price`, `rating` and `Quantity_sold`

![Alt text](Data/image.png)


### 4. Visualization based on DA:
![Alt text](Data/image-1.png)

* Requirements:
1. Sold quantity of products of large brands.
2. Comparison between Chinese-owned categories and all.
3. Correlation between rating and price of products.
4. Top 10 brands with the highest quantity of product.

### 5. Automation all process use crontab on VM and google functions.
[Script: run_scrip.sh](./src/run_scrip.sh)
[Script: Crontab_Scheduled Mongodb-gcs.txt](./src/Crontab_Scheduled.txt/)
Parameters: None

Explaination: at 20:00, the process will be run automatically.
