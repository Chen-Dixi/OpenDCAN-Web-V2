import os

allow_cors_origins = [
    "http://localhost:3000",
    "http://mystation:3000",
    "http://10.112.210.204:3000",
]

DATASET_UPLOAD_PATH="_data/"

UPLOAD_DATASET_EXTENSIONS = ['.zip', '.tar.gz', '.tar']
UPLOAD_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
RECORD_LIMIT = 10
TASK_LIST_IPP = 10
DATASET_LIST_IPP = 6

DIRIGNORE = '__MACOSX'

DATABASE_URI = os.getenv("DATABASE_URI", "localhost")
RABBITMQ_URI = os.getenv("RABBITMQ_URI", "localhost")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")