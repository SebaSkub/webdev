from flask import Flask, request
import pika

app = Flask(__name)

# RabbitMQ connection parameters
rabbitmq_host = 'sars490'  # Replace with your RabbitMQ server's hostname or IP address
queue_name = 'registration_queue'

# Initialize a connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()
channel.queue_declare(queue=queue_name)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    data = f'Registration: {username}, {password}'

    # Send registration data to RabbitMQ queue
    channel.basic_publish(exchange='', routing_key=queue_name, body=data)

    return 'Registration data sent to RabbitMQ.'

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    data = f'Login: {username}, {password}'

    # Send login data to RabbitMQ queue
    channel.basic_publish(exchange='', routing_key=queue_name, body=data)

    return 'Login data sent to RabbitMQ.'

if __name__ == '__main__':
    app.run()
