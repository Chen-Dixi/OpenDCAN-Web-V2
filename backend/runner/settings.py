import os
RABBITMQ_URI = os.getenv("RABBITMQ_URI", "localhost")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DATASET_BASE_PATH = '../'
MODEL_BASE_PATH = '../'