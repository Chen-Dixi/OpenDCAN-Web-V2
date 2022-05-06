from aio_pika import connect_robust
from aio_pika.patterns import RPC

import pika
import uuid

from settings import RABBITMQ_URI

class FastApiRpcClient(object):
    def __init__(self, host: str = RABBITMQ_URI, port: int = 5672):
        self.host = host
        self.port = port
    
    async def initialize(self):
        self.connection = await connect_robust(
            host=self.host,
            port=self.port,
            client_properties={"connection_name": "client"} #client_properties: add custom client capability.
        )

        self.channel = await self.connection.channel()
        self.rpc = await RPC.create(self.channel)
    
class SynchronousFastApiRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_URI,port=5672))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)