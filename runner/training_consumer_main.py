import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
    channel = connection.channel()

    channel.exchange_declare(exchange='dl_task', exchange_type='direct')

    que_result = channel.queue_declare(queue='', exclusive=True)
    queue_name = que_result.method.queue
    channel.queue_bind(exchange='dl_task', queue=queue_name, routing_key='train')

    print(' [*] Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))
    
    # 每个进程只接收一个训练任务！！！
    channel.basic_qos(prefetch_count=1) # quality of service
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
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