import concurrent.futures
from os.path import join

import properties


def download(item):
    properties.MINIO_CLIENT.fget_object(properties.BUCKET_NAME, item.object_name, join(properties.DOWNLOAD_FOLDER, item.object_name))
    print(item.object_name)

def run():
    objects = list(properties.MINIO_CLIENT.list_objects(properties.BUCKET_NAME, recursive=True))
    executor = concurrent.futures.ThreadPoolExecutor(5)
    futures = [executor.submit(download, item)
               for item in objects]
    concurrent.futures.wait(futures)