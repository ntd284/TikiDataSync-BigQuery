from pymongo import MongoClient
import json
import subprocess

client = MongoClient('mongodb://localhost:27017/')
DB_Name="Tiki2"
Col_Name="Tiki_info"
File = "./TikiDataSync-BigQuery/Data/Tiki_.json"
def Fetch_data_From_MongoDB():
    f = open(File, "w")

    Database = client[DB_Name]
    collection = Database[Col_Name]

    # Define the fields you want to include in the export

    cursor = collection.find()
    Data=[]
    count=0
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        if "installment_info_v2" in doc and doc["installment_info_v2"] is not None:
            doc['installment_info_v2']['details'] = str(doc['installment_info_v2'].get('details', 'Null'))
        else:
            doc['installment_info_v2'] = {'details': 'Null'}

        if "configurable_products" in doc and doc["configurable_products"] is not None:
            doc['configurable_products'][0]["size_nhan_nam"] = str(doc['configurable_products'][0].get('size_nhan_nam', 'Null'))

            
        if "configurable_products" in doc and doc["configurable_products"] is not None:
            doc['configurable_products'][0]["size_chart"] = str(doc['configurable_products'][0].get('size_chart', []))

        if "configurable_products" in doc and doc["configurable_products"] is not None:
            doc['configurable_products'][0]["chu_ky"] = str(doc['configurable_products'][0].get('chu_ky', 'Null'))

        # print(doc['configurable_products'])

        doc['crawled_time'] = str(doc.get('crawled_time', 'Null'))
        doc['add_on_title'] = str(doc.get('add_on_title', 'Null'))
        doc['add_on'] = str(doc.get('add_on', 'Null'))
        doc['has_other_fee'] = str(doc.get('has_other_fee', 'Null'))
        doc['asa_flash_swap'] = str(doc.get('asa_flash_swap', 'Null'))
        doc['badges'] = str(doc.get('badges', []))
        doc['badges_new'] = str(doc.get('badges_new', []))
        doc['category'] = str(doc.get('category', 'Null'))
        doc['status'] = str(doc.get('status', 'Null'))
        doc['asa_share_btn'] = str(doc.get('asa_share_btn', 'Null'))
        doc['confirm_over_age'] = str(doc.get('confirm_over_age', 'Null'))
        doc['errors'] = str(doc.get('errors', 'Null'))

        
        with open(File,"a",encoding="utf-8") as f:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
            count+=1
            print(f'{count}:{doc["_id"]}')
            if count == 10:
                return "Done"

def Local_data_to_GCS():

    bucket_name = 'project5-backup'
    gcs_name = 'Tiki_db.json'
    gsutil_command = [
        'gsutil',
        '-o',
        'GSUtil:parallel_composite_upload_threshold=150M',
        '-m',
        'cp',
        File,
        f'gs://{bucket_name}/{gcs_name}'
    ]
    subprocess.run(gsutil_command, check=True)
    return f'gs://{bucket_name}/{gcs_name} - DONEEE'

if __name__ == "__main__":
    Fetch_data_From_MongoDB()  

