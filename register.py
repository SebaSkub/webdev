import pika
import json
import hashlib
from flask import Flask, request

# RabbitMQ connection parameters
rabbitmq_host = 'sar490'  # Update with your RabbitMQ server host
rabbitmq_port = 5672
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
    plaintext_data = "\t".join(f"{key}={value}" for key, value in data.items())

    # Send the data as plaintext to the RabbitMQ queue
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=plaintext_data)


    # Send the data as JSON to the RabbitMQ queue
    #channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=json.dumps(data))

    connection.close()

@app.route('/register', methods=['POST'])
   def register():
    user_data = {
        'firstName': request.form.get('firstName'),
        'lastName': request.form.get('lastName'),
        'dob': request.form.get('dob'),
        'age': request.form.get('age'),
        'lolId': request.form.get('lolId'),
        'steamLink': request.form.get('steamLink'),
        'securityQuestion1': request.form.get('securityQuestion1'),
        'securityQuestion2': request.form.get('securityQuestion2'),
        'username': request.form.get('username'),
        'password': request.form.get('password')
    }

    # Process the form data as needed

    return "Registration successful"  # You can handle success and response as needed

if __name__ == '__main__':
    app.run()
