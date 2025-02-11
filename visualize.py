from os import path

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from pymongo import MongoClient
from pymongo.server_api import ServerApi

import properties


def run():
    visualization_folder = 'visualizations'
    client = MongoClient(properties.CLUSTER_URI, server_api=ServerApi('1'))
    collection = client['PPPK']['TCGA']
    documents = collection.find({})
    cohort_data = pd.DataFrame(documents)
    cohort_data.set_index('patient_id', inplace=True)
    while True:
        print("Enter offset for patient start: (max is " + str(cohort_data[cohort_data.columns[0]].count()) + "):")
        index = input()

        if index.isnumeric() and 0 <= int(index) <= cohort_data[cohort_data.columns[0]].count():
            print("Enter count: (max is 30):")
            count = input()
            if count.isnumeric() and 0 <= int(count) <= 30:
                index = int(index)
                count = int(count)
                break

    cohort_data["cancer_cohort"].value_counts(dropna=False).plot(kind="bar")
    plt.savefig(path.join(visualization_folder, 'all_bar.png'), bbox_inches='tight')
    plt.clf()
    plt.rcParams['font.size'] = 6.0

    cohort_data["cancer_cohort"].value_counts(dropna=False).sort_index().plot(kind="pie")
    plt.savefig(path.join(visualization_folder, 'all_pie.png'), bbox_inches='tight')
    plt.clf()

    cohort_data = cohort_data.drop(columns=['cancer_cohort', '_id'], axis=1)

    sns.set_context("paper")
    sns_plot = sns.clustermap(cohort_data.iloc[index : count + index], yticklabels=cohort_data.index, xticklabels=cohort_data.columns)
    sns_plot.savefig(path.join(visualization_folder, 'all_heatmap.pdf'), bbox_inches='tight')