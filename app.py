from flask import Flask, jsonify
import signal
import sys

from utils.logging_config import logger

app = Flask(__name__)


# Flask route to check status
@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "Running"}), 200


# Signal handler for graceful shutdown
def shutdown_handler(signal, frame):
    logger.info("Shutting down...")
    sys.exit(0)


if __name__ == "__main__":
    # Handle shutdown signals to clean up RabbitMQ connection
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    app.run(host="0.0.0.0", port=5001)
