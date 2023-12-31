from flask import Flask, request, jsonify, redirect
import pika

app = Flask(__name__)

# RabbitMQ configurations
rabbitmq_host = 'sars490'  # Replace with your RabbitMQ server host
rabbitmq_port = 5672
rabbitmq_user = 'it490'
rabbitmq_password = 'it490'
rabbitmq_queue = 'userLogin_FTOB'  # Replace with the name of your login queue

# Define a function to send data to RabbitMQ as plaintext
def send_to_rabbitmq(data):
    try:
        # Initialize a connection to RabbitMQ
        credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue=rabbitmq_queue, durable=True)

        # Send the data to RabbitMQ in the desired format
        channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=data)

        # Close the connection
        connection.close()

    except Exception as e:
        # Handle exceptions if the connection or message sending fails
        print(f"Failed to send data to RabbitMQ: {str(e)}")

# Your login route
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            # Assuming valid login, send data to RabbitMQ in the desired format
            login_data = f'{username},{password}'
            send_to_rabbitmq(login_data)
            return redirect('/it490/landing.html')


        except Exception as e:
            return 'Login failed', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7007)
