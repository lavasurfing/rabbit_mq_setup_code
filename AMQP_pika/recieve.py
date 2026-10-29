import os

import pika


def main():
    host = os.environ.get("RABBITMQ_HOST", "127.0.0.1")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    channel.queue_declare(
        queue="hello", durable=True, arguments={"x-queue-type": "quorum"}
    )

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")

    channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)
    print(" [*] Waiting for messages. To exit press CTRL+C")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print(" [x] Interrupted")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
