from aio_pika import connect_robust
from aio_pika.patterns import RPC

from repository.database import SessionLocal
from repository import crud
from settings import RABBITMQ_URI

__all__ = [
    'rpc_router_start_training',
    'rpc_router_finish_training'
]


def model_start_training(*, model_id: int):
    db = SessionLocal()
    crud.update_model_record_by_id(db, model_id, {"state": 3}, auto_commit=True) # update to training
    db.close()
    return 0

async def rpc_router_start_training(loop):
    
    connection = await connect_robust(host=RABBITMQ_URI, port=5672, loop=loop)
    channel = await connection.channel()

    rpc = await RPC.create(channel)
    
    # register method
    await rpc.register('model_start_training', model_start_training, auto_delete=True)
    print('Established pika async listener')
    return connection

def model_finish_training(*,task_id: int, model_id: int, file_path:str, state: int):
    db = SessionLocal()
    toUpdate = {"state": state}
    task_state = 1
    if state == 1: # model ready
        task_state = 3 # then task ready
        toUpdate["file_path"] = file_path

    crud.update_model_record_by_id(db, model_id, toUpdate, auto_commit=False) # update to training
    crud.update_task_record_by_id(task_id, {"state": task_state}, db, auto_commit=False)
    db.commit()
    db.close()
    return 0

async def rpc_router_finish_training(loop):
    connection = await connect_robust(host=RABBITMQ_URI, port=5672, loop=loop)
    channel = await connection.channel()

    rpc = await RPC.create(channel)

    # register method
    await rpc.register('model_finish_training', model_finish_training, auto_delete=True)
    print('Established pika async listener')
    return connection