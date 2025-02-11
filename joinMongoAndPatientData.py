import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import properties


def run():
    while True:
        print("Enter path to patient file: ")
        patient_path = input()
        if patient_path.endswith(".tsv"):
            data = pd.read_csv(patient_path, sep='\t', header=0)
            if len(data) > 0 and 'bcr_patient_barcode' in data.columns and 'DSS' in data.columns and 'OS' in data.columns and 'clinical_stage' in data.columns:
                break

    client = MongoClient(properties.CLUSTER_URI, server_api=ServerApi('1'))
    collection = client['PPPK']['TCGA']
    try:
        data = data[['bcr_patient_barcode', 'DSS', 'OS', 'clinical_stage']]
        data.rename(columns={'bcr_patient_barcode': 'patient_id'}, inplace=True)
        documents = collection.find({})
        cohort_data = pd.DataFrame(documents)
        print(cohort_data.head())
        print(data.head())
        merged = pd.merge(cohort_data, data, how='inner', on=['patient_id'])
        merged = merged.drop('_id', axis=1)
        print(merged.head())

        collection_patients = client['PPPK']['TCGA_PATIENTS']
        records = merged.to_dict(orient='records')
        collection_patients.insert_many(records)
    except Exception as e:
        print(e)
