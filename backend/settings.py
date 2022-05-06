import os
allow_cors_origins = [
    "http://localhost:3000"
]

DATASET_UPLOAD_PATH="_data/"

UPLOAD_DATASET_EXTENSIONS = ['.zip', '.tar.gz', '.tar']
RECORD_LIMIT = 10
TASK_LIST_IPP = 10
DATASET_LIST_IPP = 6

DIRIGNORE = '__MACOSX'

DATABASE_URI = os.getenv("DATABASE_URI", "localhost")
RABBITMQ_URI = os.getenv("RABBITMQ_URI", "localhost")