import os
import sys
import pika

host = os.environ.get("RABBITMQ_HOST", "127.0.0.1")
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))

channel = connection.channel()

channel.queue_declare(queue='hello', durable=True, arguments={'x-queue-type': 'quorum'})

# message = ' '.join(sys.argv[1:]) or "Hello World!"

work_array = ["work1.........", "work2....", "work3...."]
for work in work_array:
    channel.basic_publish(
        exchange='',
        routing_key='hello',
        body=work,
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent
        )
    )
    print(f" [x] Sent {work}")