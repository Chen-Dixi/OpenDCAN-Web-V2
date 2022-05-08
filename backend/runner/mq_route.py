import os

import pickle
import asyncio
from aio_pika import connect_robust
from aio_pika.patterns import RPC
from numpy import record

from rpc_client import FastApiRpcClient

__all__ = [
    'training_consumer'
]

async def test():
    aio_rpc_client = FastApiRpcClient() # 使用默认配置
    await aio_rpc_client.initialize()
    res = await aio_rpc_client.rpc.proxy.remote_method(task_id=2, model_id = 5)
    return res

async def test2():
    aio_rpc_client = FastApiRpcClient() # 使用默认配置
    await aio_rpc_client.initialize()
    res = await aio_rpc_client.rpc.proxy.remote_method2(task_id=2, model_id = 5)
    return res

async def training_ack(model_id: int):
    aio_rpc_client = FastApiRpcClient() # 使用默认配置
    await aio_rpc_client.initialize()
    res = await aio_rpc_client.rpc.proxy.model_start_training(model_id = model_id)
    return res

async def finish_training_ack(task_id: int, model_id: int, file_path:str, state: int):
    aio_rpc_client = FastApiRpcClient() # 使用默认配置
    await aio_rpc_client.initialize()
    res = await aio_rpc_client.rpc.proxy.model_finish_training(task_id = task_id, model_id = model_id, file_path = file_path, state = state)
    return res

def training_consumer(ch, method, properties, body):
    """Entrance of rabbitmq message
    body needs to be loaded by pickle
    {
        'source_path': db_source.file_path,
        'target_path': db_target.file_path,
        'model_id': db_model_record.id,
        'task_id': createDto.task_id,
    }
    """
    body = pickle.loads(body)
    print(" [x] %r:%r" % (method.routing_key, body))
    source_path = body['source_path']
    target_path = body['target_path']
    model_id = body['model_id']
    task_id = body['task_id']

    response = asyncio.run(training_ack(model_id))

    print(" [x] Get response:%d" % (response))
    checkpoint_dir = '_model/task_%d/model_%d/' % (task_id, model_id)
    checkpoint_file_name = 'latest.pth.tar'
    pid = os.fork()
    if pid == 0:
        # 子进程
        env = dict(os.environ)
        os.execlpe('python', 'python', 
        'main_train.py', 
        '--source_path', source_path, 
        '--target_path', target_path, 
        '--task_id', str(task_id),
        '--model_id', str(model_id),
        '--checkpoint_dir', checkpoint_dir,
        '--checkpoint_file_name', checkpoint_file_name,
        env)
        # os.execlpe('python', 'python', 'test.py', env)
    else:
        childProcExitInfo = os.wait()
        # os.waitstatus_to_exitcode(childProcExitInfo[1]) # if python==3.9
        exit_code = childProcExitInfo[1] >> 8
        if exit_code == 1:
            response = asyncio.run(finish_training_ack(task_id, model_id, checkpoint_dir+checkpoint_file_name, 4))
        elif exit_code == 0:
            response = asyncio.run(finish_training_ack(task_id, model_id, checkpoint_dir+checkpoint_file_name, 1))
        print("Child process exit code: %d"%(exit_code))

def inference_consumer(ch, method, properties, body):
    pass