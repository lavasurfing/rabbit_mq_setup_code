import os

import pika

host = os.environ.get("RABBITMQ_HOST", "127.0.0.1")
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))

channel = connection.channel()

channel.queue_declare(queue='hello', durable=True, arguments={'x-queue-type': 'quorum'})

channel.basic_publish(
    exchange='',
    routing_key='hello',
    body='Gettting messages from RabbitMQ'
)

print(" [x] Sent 'Hello World!'")

connection.close()