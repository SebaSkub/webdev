import pika
import json
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

    # Send the data as JSON to the RabbitMQ queue
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=json.dumps(data))

    connection.close()


def send_to_rabbitmq(data):
    try:
         Publish the user registration data to the RabbitMQ queue
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(data),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make the message persistent
            )
        
        print(" [x] Sent user data to RabbitMQ")
   except Exception as e:
        print(f"An error occurred: {e}")




@app.route('/register', methods=['POST'])
def register():
    user_data = request.json  # Assuming the data is received as JSON

    #Send user data to RabbitMQ
    send_to_rabbitmq(user_data)

    return "Registration successful"

if __name__ == '__main__':
    app.run()
