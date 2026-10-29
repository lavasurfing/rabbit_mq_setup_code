import pika
import time
import os

host = os.environ.get("RABBITMQ_HOST", "127.0.0.1")
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True, arguments={'x-queue-type': 'quorum'})
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='hello', on_message_callback=callback)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print(' [x] Interrupted')
    channel.stop_consuming()
finally:
    connection.close()