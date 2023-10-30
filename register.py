# Import necessary libraries
from flask import Flask, request, render_template
import pika
from pika.credentials import PlainCredentials as PikaCredentials
import json

app = Flask(__name)

# Configure RabbitMQ connection parameters
rabbitmq_host = '10.198.120.114'  # Update with your RabbitMQ server host
rabbitmq_port = 5672
rabbitmq_user = 'it490'
rabbitmq_password = 'it490'
rabbitmq_queue = 'userRegister_FTOB'

# Define a function to send data to RabbitMQ
def send_to_rabbitmq(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=rabbitmq_queue)
    credentials = PikaCredentials(rabbitmq_user, rabbitmq_password)

    

    # Convert data to JSON
    message = json.dumps(data)

    # Send the data to the RabbitMQ queue
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=message)

    connection.close()

# Define a route to handle the form submission
@app.route('/it490/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # Get form data
        data = {
            'type': 'register',
            'email': request.form.get('email'),
            'first_name': request.form.get('first'),
            'last_name': request.form.get('last'),
            'DOB': request.form.get('DOB'),
            'age': request.form.get('age'),
            'lol_id': request.form.get('lolID'),
            'steam_link': request.form.get('steamLink'),
            'sec_question_1': request.form.get('secQuest1'),
            'sec_question_2': request.form.get('secQuest2'),
            'username': request.form.get('user'),
            'password': request.form.get('pass')
        }

        try:
            # Send data to RabbitMQ
            send_to_rabbitmq(data)
            return "User registration submitted successfully."
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port 5672)
