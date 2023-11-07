from flask import Flask, request, jsonify
import pika

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
channel.queue_declare(queue=rabbitmq_queue, durable=True)

# Define a function to send data to RabbitMQ as plaintext
def send_to_rabbitmq(data):
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=data)

# Your login route
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            # Assuming valid login, send data to RabbitMQ in the desired format
            login_data = f'Username: {username}, Password: {password}'
            send_to_rabbitmq(login_data)

            return 'Login successful', 200

        except Exception as e:
            return 'Login failed', 400
if __name__ == '__main__':
    app.run(host='10.198.120.126', port=7007)
