from flask import Flask, request
import pika
import json

app = Flask(__name)

rabbitmq_host = 'sar490'  # Update with your RabbitMQ server host
rabbitmq_port = 5672
rabbitmq_user = 'it490'
rabbitmq_password = 'it490'
rabbitmq_queue = 'userLogin_FTOB'

# Define a function to send data to RabbitMQ
def send_to_rabbitmq(data):
    # Configure the RabbitMQ connection
    credentials = PikaCredentials(username = rabbitmq_user, password = rabbitmq_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials))
    channel = connection.channel()

    # Declare a queue for login data
    channel.queue_declare(queue='login_queue')

    # Send the data as JSON to the RabbitMQ queue
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=str(data))

    connection.close()

# Define a route to handle the form submission
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        # Get the login data from the request
        login_data = request.form

        # Process the login data if needed

        # Send the login data to RabbitMQ as plaintext
        send_to_rabbitmq(login_data)

        return 'Login data sent to RabbitMQ'
