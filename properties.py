from minio import Minio

ACCESS_KEY = "minioAdmin"
SECRET_KEY = "supersecretpassword"
MINIO_CLIENT = Minio("regoch.net:9000", access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)
BUCKET_NAME = "josip-pufler"
TARGET_GENES = ["C6orf150", "cGAS", "CCL5", "CXCL10", "TMEM173", "STING", "CXCL9", "CXCL11", "NFKB1", "IKBKE", "IRF3", "TREX1", "ATM", "IL6", "IL8", "CXCL8"]
CLUSTER_URI = "mongodb+srv://jpufler:8VdI9gh5CTwQei7U@cluster0.tyqbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DOWNLOAD_FOLDER = 'bucketData'