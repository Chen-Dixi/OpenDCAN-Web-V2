import os

if __name__ == '__main__':
    # pid = os.fork()
    # if pid == 0:
    #     # 子进程
    #     env = dict(os.environ)
    #     os.execlpe('python', 'python', 
    #     'main_train.py', 
    #     # '--source_path', 'data/test1', 
    #     # '--target_path', 'data/test2', 
    #     '--task_id', '1',
    #     '--record_id', '2',
    #     env)
        
    # else:
    #     childProcExitInfo = os.wait()
    #     print("Child process exit statu: %d"%(childProcExitInfo[1]))
    #     print("Child process %d exited"%(childProcExitInfo[0]))
    #     print("Parent process %d exiting after child has exited"%(os.getpid()))

    os._exit(0)