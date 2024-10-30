from flask import Flask, jsonify
from threading import Thread

from utils.rabbit_connection import RabbitMQClient

app = Flask(__name__)


def start_rabbitmq_listener():
    rabbitmq_client = RabbitMQClient()
    rabbitmq_client.connect()

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    rabbitmq_client.start_consuming(callback)


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "Running"}), 200


if __name__ == "__main__":
    listener_thread = Thread(target=start_rabbitmq_listener)
    listener_thread.daemon = True
    listener_thread.start()
    app.run(host="0.0.0.0", port=5001)
