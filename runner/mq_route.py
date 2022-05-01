import pickle
import os

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
    # print(" [x] %r:%r" % (method.routing_key, body))
    source_path = body['source_path']
    target_path = body['target_path']
    model_id = body['model_id']
    task_id = body['task_id']
    
    pid = os.fork()
    if pid is 0:
        # 子进程
        env = dict(os.environ)
        os.execlpe('python', 'python', 'main_train.py', '--source-path', source_path, '--target-path', target_path, env)
        
    else:
        childProcExitInfo = os.wait()
        print("Child process exit statu: %d"%(childProcExitInfo[1]))
        print("Child process %d exited"%(childProcExitInfo[0]))