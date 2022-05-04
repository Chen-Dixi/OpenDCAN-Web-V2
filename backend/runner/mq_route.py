import pickle
import asyncio
from aio_pika import connect_robust
from aio_pika.patterns import RPC

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
    
    response = asyncio.run(test())

    print(" [x] Get response:%d" % (response))

    response = asyncio.run(test2())

    print(" [x] Get response2:%d" % (response))
    # pid = os.fork()
    # if pid is 0:
    #     # 子进程
    #     env = dict(os.environ)
    #     os.execlpe('python', 'python', 'main_train.py', '--source-path', source_path, '--target-path', target_path, env)
        
    # else:
    #     childProcExitInfo = os.wait()
    #     print("Child process exit statu: %d"%(childProcExitInfo[1]))
    #     print("Child process %d exited"%(childProcExitInfo[0]))