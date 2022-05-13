import pika
from aio_pika import connect_robust
import pickle

from settings import RABBITMQ_URI
# def get_mq_channel():
#     connection = pika.BlockingConnection(
#         pika.ConnectionParameters(host='localhost',port=5672)
#     )
#     channel = connection.channel()
#     channel.exchange_declare(exchange='dl_task', exchange_type='direct')

#     try:
#         yield channel
#     finally:
#         connection.close()

class PikaPublisher(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_URI,port=5672)
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='dl_task', exchange_type='direct')
    
    def send_training_task(self, message: dict):
        self.channel.basic_publish(
            exchange='dl_task',
            routing_key='train',
            body=pickle.dumps(message))
    
    def send_dataset_label(self, message: dict):
        self.channel.basic_publish(
            exchange='dl_task',
            routing_key='inference_dataset',
            body=pickle.dumps(message))
    
    def send_sample_label(self, message: dict):
        self.channel.basic_publish(
            exchange='dl_task',
            routing_key='inference_sample',
            body=pickle.dumps(message))
    
    # 定义 fastapi server 的rpc接口
    async def rpc_server(self, loop):
        """Usage: RPC Interface for updating model record's state

        """
        connection = await connect_robust(host=RABBITMQ_URI, port=5672, loop=loop)
        channel = await connection.channel()

        queue = await channel.declare_queue(name='rpc_server_queue')

    def close(self):
        self.connection.close()