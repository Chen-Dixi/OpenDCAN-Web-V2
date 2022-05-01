import pika, sys, os
from mq_route import training_consumer # rabbitmq 和 训练代码之间的接口函数

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
    channel = connection.channel()

    channel.exchange_declare(exchange='dl_task', exchange_type='direct')

    # 用一个临时的队列就行了
    que_result = channel.queue_declare(queue='', exclusive=True)
    queue_name = que_result.method.queue
    channel.queue_bind(exchange='dl_task', queue=queue_name, routing_key='train')

    print(' [*] Waiting for messages. To exit press CTRL+C')
    
    # 每个进程只接收一个训练任务！！！ 设置 quality-of-service
    channel.basic_qos(prefetch_count=1) # quality of service
    channel.basic_consume(queue = queue_name, on_message_callback = training_consumer, auto_ack = True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)