import pika
import os
from dotenv import load_dotenv
from utils.logging_config import logger

load_dotenv()

game_events_queue = os.getenv("QUEUE_NAME")
queue_host = os.getenv("QUEUE_HOST")
queue_port = int(os.getenv("QUEUE_PORT"))
queue_user = os.getenv("QUEUE_USER")
queue_pass = os.getenv("QUEUE_PASS")
queue_exchange = os.getenv("EXCHANGE_NAME")
queue_routing_key = os.getenv("ROUTING_KEY")

connection_params = pika.ConnectionParameters(
    host=queue_host,
    port=queue_port,
    virtual_host=queue_user,
    credentials=pika.PlainCredentials(queue_user, queue_pass, erase_on_connect=True),
)


class RabbitMQClient:
    def __init__(self):
        self.queue_name = game_events_queue
        self.connection_params = connection_params
        self.connection = None
        self.channel = None

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(self.connection_params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            logger.info("Connected to RabbitMQ")
        except pika.exceptions.AMQPError as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            self.close()

    def close(self):
        try:
            if self.channel:
                self.channel.close()
            if self.connection:
                self.connection.close()
            logger.info("Closed RabbitMQ connection")
        except pika.exceptions.AMQPError as e:
            logger.error(f"Error closing RabbitMQ connection: {e}")

    def start_consuming(self, callback):
        try:
            self.channel.basic_consume(
                queue=self.queue_name, on_message_callback=callback, auto_ack=True
            )
            logger.info(" [*] Waiting for messages. To exit press CTRL+C")
            self.channel.start_consuming()
        except pika.exceptions.AMQPError as e:
            logger.error(f"Error in message consumption: {e}")
            self.close()

    def publish_message(self, message):
        try:
            self.channel.basic_publish(
                exchange=queue_exchange, routing_key=queue_routing_key, body=message
            )
            logger.info("Message published successfully")
        except pika.exceptions.AMQPError as e:
            logger.error(f"Failed to publish message: {e}")
            self.close()
