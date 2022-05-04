
from aio_pika import connect_robust
from aio_pika.patterns import RPC

from fastapi.logger import logger

from repository.database import SessionLocal
from repository import crud
from domain import task_service

__all__ = [
    'consume'
]

def remote_method(*, task_id: int, model_id: int):
    # DO SOMETHING
    # Move this method along with others to another place e.g. app/rpc_methods
    # I put it here for simplicity
    return task_id + model_id

async def consume(loop):
    connection = await connect_robust(host='localhost', port=5672, loop=loop)
    channel = await connection.channel()

    rpc = await RPC.create(channel)
    
    # register method
    await rpc.register('remote_method', remote_method, auto_delete=True)
    print('Established pika async listener')
    return connection

def remote_method2(*, task_id: int, model_id: int):
    # DO SOMETHING
    # Move this method along with others to another place e.g. app/rpc_methods
    # I put it here for simplicity
    return task_id + model_id

async def consume2(loop):
    connection = await connect_robust(host='localhost', port=5672, loop=loop)
    channel = await connection.channel()

    rpc = await RPC.create(channel)
    
    # register method
    await rpc.register('remote_method2', remote_method2, auto_delete=True)
    print('Established pika async listener')
    return connection

def model_start_training(*, model_id: int):
    db = SessionLocal()
    crud.update_model_record_by_id(db, model_id, {"state": 3}) # update to training
    db.close()
    return 0

async def consume(loop):
    
    connection = await connect_robust(host='localhost', port=5672, loop=loop)
    channel = await connection.channel()

    rpc = await RPC.create(channel)
    
    # register method
    await rpc.register('model_start_training', model_start_training, auto_delete=True)
    print('Established pika async listener')
    return connection