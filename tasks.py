import os
from celery import Celery
from utils.rabbit_connection import RabbitMQClient

broker_url = os.getenv("CELERY_BROKER_URL")
app = Celery('tasks', broker=broker_url)

@app.task
def process_message(body):
    print(f"Procesing message: {body}")