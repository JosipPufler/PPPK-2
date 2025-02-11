import concurrent.futures
import concurrent.futures
import os
from os import listdir
from os.path import isfile, join

import properties

def upload(folder_path, file):
    properties.MINIO_CLIENT.fput_object(properties.BUCKET_NAME, file, join(folder_path, file), "application/text")
    print(file)

def run():
    while True:
        print("Enter path to folder containing .tsv files: ")
        folder_path = input()
        if os.path.exists(os.path.dirname(folder_path)):
            break

    found = properties.MINIO_CLIENT.bucket_exists(properties.BUCKET_NAME)
    if not found:
       properties.MINIO_CLIENT.make_bucket(properties.BUCKET_NAME)
    else:
       print("Bucket already exists")
    only_files = [f for f in listdir(folder_path) if isfile(join(folder_path, f)) and f.endswith(".tsv")]
    executor = concurrent.futures.ThreadPoolExecutor(2)
    futures = [executor.submit(upload, folder_path, file) for file in only_files]
    concurrent.futures.wait(futures)

    print("It is successfully uploaded to bucket")