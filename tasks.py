import os
from celery import Celery
from utils.logging_config import logger

broker_url = os.getenv("CELERY_BROKER_URL")
app = Celery("tasks", broker=broker_url)


@app.task(bind=True)
def process_message(self, body):
    try:
        logger.info(f"Processing message: {body}")
        # Add processing logic here
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        self.retry(exc=e, countdown=5)  # Retry if error occurs
