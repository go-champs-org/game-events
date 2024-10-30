from dotenv import load_dotenv
from utils.rabbit_connection import RabbitMQClient

load_dotenv()

rabbitmq_client = RabbitMQClient()
rabbitmq_client.connect()


rabbitmq_client.publish_message("Hello World")
print(" [x] Sent 'Hello World!'")
rabbitmq_client.close()
