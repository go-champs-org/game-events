from utils.logging_config import logger
from utils.rabbit_connection import RabbitMQClient
from tasks import process_message
import signal
import sys
import time


# RabbitMQ client instance
rabbitmq_client = RabbitMQClient()
is_running = True  # Flag to control the listener loop


def start_rabbitmq_listener():
    while is_running:
        try:
            rabbitmq_client.connect()
            logger.info("Connected to RabbitMQ, starting to consume messages.")

            def callback(ch, method, properties, body):
                logger.info("Message received. Forwarding to Celery.")
                process_message.delay(body)  # Send message to Celery

            rabbitmq_client.start_consuming(callback)
        except Exception as e:
            if is_running:  # Only log if it's not shutting down
                logger.error(f"Error in RabbitMQ listener: {e}")
                rabbitmq_client.close()
                logger.info("Attempting to reconnect in 5 seconds...")
                time.sleep(5)  # Wait before trying to reconnect


def handle_shutdown(signum, frame):
    global is_running
    is_running = False  # Stop the loop
    logger.info("Received shutdown signal. Closing RabbitMQ connection...")
    rabbitmq_client.close()
    logger.info("RabbitMQ connection closed. Exiting.")
    sys.exit(0)


# Register signal handlers for graceful shutdown
signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)

if __name__ == "__main__":
    start_rabbitmq_listener()
