import pika
from flask import Flask, request, render_template
import json

# RabbitMQ connection parameters
rabbitmq_host = 'sars490'  # Update with your RabbitMQ server host
rabbitmq_port = 5672
rabbitmq_user = 'it490'
rabbitmq_password = 'it490'
rabbitmq_queue = 'userRegister_FTOB'

app = Flask(__name)

def send_to_rabbitmq(data):
    # Configure the RabbitMQ connection
    credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials))
    channel = connection.channel()
    message = 'Hello, RabbitMQ!'

    # Declare a queue for user registration data
    channel.queue_declare(queue=rabbitmq_queue, durable=True)

    # Send the data as JSON to the RabbitMQ queue
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=json.dumps(data), message)

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

    # Send user registration data to RabbitMQ
    send_to_rabbitmq(user_data)

    return "Registration successful"  # You can handle success and response as needed

if __name__ == '__main__':
    app.run()
