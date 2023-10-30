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
    channel.basic_publish(exchange='', routing_key='login_queue', body=json.dumps(data))

    connection.close()

# Define a route to handle the form submission
@app.route('/', methods=['POST'])
def login():
    # Get form data
    data = {
        'type': 'login',
        'user': request.form['user'],
        'pass': request.form['pass']
    }

    # Send data to RabbitMQ
    send_to_rabbitmq(data)

    # Redirect to a success page or handle the response as needed
    return redirect ('/it490/landing.html')

if __name__ == '__main__':
    app.run()
