from os import listdir
from os.path import isfile, join

import matplotlib.pyplot as plt
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import properties


def run():
    combined_data = pd.DataFrame()
    only_files = [f for f in listdir(properties.DOWNLOAD_FOLDER) if isfile(join(properties.DOWNLOAD_FOLDER, f)) and f.endswith(".tsv")]
    for file in only_files:
        data = pd.read_csv(join(properties.DOWNLOAD_FOLDER, file), sep='\t', header=0)
        data = data[data['sample'].isin(properties.TARGET_GENES)]
        data.set_index('sample', inplace=True)
        data = data.transpose()
        data.reset_index(drop=False, inplace=True)

        data.rename(columns={'index': 'patient_id'}, inplace=True)
        data.index.names = ['index']
        data['cancer_cohort'] = file.split('.')[0]
        data['patient_id'] = data['patient_id'].apply(lambda x: str(x)[:-3])
        combined_data = pd.concat([combined_data, data], ignore_index=True)
        print(file)

    client = MongoClient(properties.CLUSTER_URI, server_api=ServerApi('1'))
    collection = client['PPPK']['TCGA']
    try:
        records = combined_data.to_dict(orient='records')
        collection.insert_many(records)
    except Exception as e:
        print(e)