from flask import Flask, request, jsonify
import pika
import json

app = Flask(__name)
# RabbitMQ configurations
rabbitmq_host = 'sars490'  # Replace with your RabbitMQ server host
rabbitmq_port = 5672
rabbitmq_user = 'it490'
rabbitmq_password = 'it490'
rabbitmq_queue = 'userLogin_FTOB'  # Replace with the name of your login queue

# Initialize a connection to RabbitMQ
credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue=rabbitmq_queue, durable = True)

# Define a function to send data to RabbitMQ as plaintext
def send_to_rabbitmq(data):
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=data)

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('user')
            password = request.form.get('pass')

            # Validate user's credentials (you can implement your own validation logic here)
            # For example, check if the username and password are correct

            if username == 'user' and password == 'pass':
                # Assuming valid login, send data to RabbitMQ
                login_data = f"{username}, {password}"
                send_to_rabbitmq(login_data)
                return redirect('/it490/landing.html')

            else:
                return 'Invalid username or password', 401

        except Exception as e:
            return 'Login failed', 400

if __name__ == '__main__':
    app.run()
