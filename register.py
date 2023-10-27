from flask import Flask, request, render_template
import pika
import json

app = Flask(__name)

# Define a function to send data to RabbitMQ
def send_to_rabbitmq(data):
    # Configure the RabbitMQ connection
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # Declare a queue for registration data
    channel.queue_declare(queue='registration_queue')
    
    # Send the data as JSON to the RabbitMQ queue
    channel.basic_publish(exchange='',
                          routing_key='registration_queue',
                          body=json.dumps(data))
    
    connection.close()

# Define a route to handle the form submission
@app.route('/register', methods=['POST'])
def register():
    # Get form data
    data = {
        'type': 'register',
        'email': request.form['email'],
        'first': request.form['first'],
        'last': request.form['last'],
        'user': request.form['user'],
        'pass': request.form['pass']
    }
    
    # Send data to RabbitMQ
    send_to_rabbitmq(data)
    
    # Redirect to a success page or handle the response as needed
    return "User registration submitted successfully."

if __name__ == '__main__':
    app.run()
