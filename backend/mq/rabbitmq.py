import pika
import json

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
            pika.ConnectionParameters(host='localhost',port=5672)
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='dl_task', exchange_type='direct')
    
    def send_training_task(self, message: dict):
        self.channel.basic_publish(
            exchange='dl_task',
            routing_key='train',
            body=json.dumps(message))
    
    def send_dataset_label(self, message: dict):
        self.channel.basic_publish(
            exchange='dl_task',
            routing_key='inference_dataset',
            body=json.dumps(message))
    
    def send_sample_label(self, message: dict):
        self.channel.basic_publish(
            exchange='dl_task',
            routing_key='inference_sample',
            body=json.dumps(message))