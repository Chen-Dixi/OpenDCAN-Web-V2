from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import user, dataset, task, base_router
from settings import allow_cors_origins
from mq.rabbitmq import PikaPublisher
# create database table, skip this if there already has one
# entity.Base.metadata.create_all(bind=engine)

class DixiFastAPI(FastAPI):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_publisher = PikaPublisher()

# app = FastAPI(docs_url='/api/v1/docs')
app = DixiFastAPI(docs_url='/api/v1/docs')
app.include_router(base_router.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(dataset.router, prefix="/api/v1")
app.include_router(task.router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)