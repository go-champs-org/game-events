import pika, os
from dotenv import load_dotenv

load_dotenv()

game_events_queue = os.getenv("QUEUE_NAME")
queue_host = os.getenv("QUEUE_HOST")
queue_port = int(os.getenv("QUEUE_PORT"))
queue_user = os.getenv("QUEUE_USER")
queue_pass = os.getenv("QUEUE_PASS")

connection_params = pika.ConnectionParameters(
    host=queue_host,
    port=queue_port,
    virtual_host=queue_user,
    credentials=pika.PlainCredentials(queue_user, queue_pass),
)


class RabbitMQClient:
    def __init__(self):
        self.queue_name = game_events_queue
        self.connection_params = connection_params
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def close(self):
        if self.connection:
            self.connection.close()

    def start_consuming(self, callback):
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback, auto_ack=True
        )
        print(" [*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def publish_message(self, message):
        self.channel.basic_publish(
            exchange="game-events", routing_key="game-id", body=message
        )