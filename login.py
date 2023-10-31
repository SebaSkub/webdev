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
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=data)

    connection.close()

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            # Validate user's credentials (you can implement your own validation logic here)
            # For example, check if the username and password are correct

            if username == 'example_username' and password == 'example_password':
                # Assuming valid login, send data to RabbitMQ
                login_data = f'Username: {username}, Password: {password}'
                send_to_rabbitmq(login_data)
                return 'Login successful', 200
            else:
                return 'Invalid username or password', 401

        except Exception as e:
            return 'Login failed', 400

if __name__ == '__main__':
    app.run()
