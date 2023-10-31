from flask import Flask, request, jsonify
import pika
import json

app = Flask(__name)

rabbitmq_host = 'sars490'  # Update with your RabbitMQ server host
rabbitmq_port = 5672
rabbitmq_user = 'it490'
rabbitmq_password = 'it490'
rabbitmq_queue = 'userLogin_FTOB'

# Define a function to send data to RabbitMQ
def send_to_rabbitmq(data):
    # Configure the RabbitMQ connection
    credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials))
    channel = connection.channel()

    # Declare a queue for login data
    channel.queue_declare(queue=rabbitmq_queue)

    # Send the data as JSON to the RabbitMQ queue
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=json.dumps(data))

    connection.close()

# Your login route
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()  # Get the JSON data from the request
        # Validate user's credentials (you can implement your own validation logic here)

        # Assuming valid login, send data to RabbitMQ
        send_to_rabbitmq(data)

        return 'Login successful', 200

    except Exception as e:
        return 'Login failed', 400

if __name__ == '__main__':
    app.run()
