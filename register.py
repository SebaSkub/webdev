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
    
@app.route('/register', methods=['POST'])
def register():
    user_data = {
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName'],
        'dob': request.form['dob'],
        'age': request.form['age'],
        'lolId': request.form['lolId'],
        'steamLink': request.form['steamLink'],
        'securityQuestion1': request.form['securityQuestion1'],
        'securityQuestion2': request.form['securityQuestion2'],
        'username': request.form['username'],
        'password': request.form['password']
    }

    # Convert the data to a string
    data_string = "\t".join(f"{key}={value}" for key, value in user_data.items())

    # Publish the data to the RabbitMQ queue
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=data_string)

    # Close the connection
    connection.close()

    return "Registration successful"

if __name__ == '__main__':
    app.run(debug=True)
