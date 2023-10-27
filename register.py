from flask import Flask, request
import pika
import json

app = Flask(__name)

# Configure RabbitMQ connection parameters
rabbitmq_host = 'sar490'  # Update with your RabbitMQ server host
rabbitmq_queue = 'registration_queue'

# Define a function to send data to RabbitMQ
def send_to_rabbitmq(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    
    # Declare a queue for registration data
    channel.queue_declare(queue=rabbitmq_queue)
    
    # Send the data as JSON to the RabbitMQ queue
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=json.dumps(data))
    
    connection.close()

# Define a route to handle the form submission
@app.route('/', methods=['POST'])
def register():
    # Get form data
    email = request.form.get('email')
    first_name = request.form.get('first')
    last_name = request.form.get('last')
    username = request.form.get('user')
    password = request.form.get('pass')

    # Create a dictionary with form data
    data = {
        'type': 'register',
        'email': email,
        'first': first_name,
        'last': last_name,
        'user': username,
        'pass': password
    }

    # Send data to RabbitMQ
    send_to_rabbitmq(data)

    # Print form data to the console (optional)
    print(f"Email: {email}")
    print(f"First Name: {first_name}")
    print(f"Last Name: {last_name}")
    print(f"Username: {username}")
    print(f"Password: {password}")

    # You can process and store the data as needed here

    # Redirect to a success page or handle the response as needed
    return "User registration submitted successfully."

if __name__ == '__main__':
    app.run()
