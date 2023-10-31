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

# Establish a connection to RabbitMQ
def send_to_rabbitmq(data):
    # Configure the RabbitMQ connection
    credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials))
    channel = connection.channel()

    # Declare a queue for login data
    channel.queue_declare(queue=rabbitmq_queue, durable=True)

    # Send the data as plaintext to the RabbitMQ queue
    plaintext_data = "\t".join(f"{key}={value}" for key, value in data.items())
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=plaintext_data)

    connection.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
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

        # Process the form data as needed
        send_to_rabbitmq(user_data)

        return "Registration successful"  # You can handle success and response as needed
    else:
        return render_template('/it490/register.html')  # Render the HTML form

if __name__ == '__main__':
    app.run()
