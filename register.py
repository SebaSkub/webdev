import pika
import json
import hashlib
from flask import Flask, request

# RabbitMQ connection parameters
rabbitmq_host = 'sar490'  # Update with your RabbitMQ server host
rabbitmq_port = 15672
rabbitmq_user = 'it490'
rabbitmq_password = 'it490'
rabbitmq_queue = 'userRegister_FTOB'

app = Flask(__name)

# Establish a connection to RabbitMQ
def send_to_rabbitmq(data):
    # Configure the RabbitMQ connection
    credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials))
    channel = connection.channel()

    # Declare a queue for login data
    channel.queue_declare(queue=rabbitmq_queue, durable = True)
    serialized_data = "\t".join(str(value) for value in data.values())
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=serialized_data)


    # Send the data as JSON to the RabbitMQ queue
    #channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=json.dumps(data))

    connection.close()

@app.route('/register', methods=['POST'])
def register():
    user_data = request.form  # Assuming the data is received as form data

    # Hash the password before sending it to RabbitMQ
    if 'password' in user_data:
        password = user_data['password']
        user_data['password'] = hashlib.sha256(password.encode()).hexdigest()  # Hash the password

    # Send user data to RabbitMQ
    send_to_rabbitmq(user_data)

    return "Registration successful"

if __name__ == '__main__':
    app.run()
