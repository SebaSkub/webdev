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
    # Configure the RabbitMQ connection
    credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials))
    channel = connection.channel()
    # Declare a queue for user registration data
    channel.queue_declare(queue=rabbitmq_queue, durable=True)

    
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # Collect form data
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        dob = request.form['dob']
        age = request.form['age']
        lol_id = request.form['lolId']
        steam_link = request.form['steamLink']
        security_question1 = request.form['securityQuestion1']
        security_question2 = request.form['securityQuestion2']
        username = request.form['username']
        password = request.form['password']

        # Prepare the data as a plaintext message
        registration_data = f"First Name: {first_name}\nLast Name: {last_name}\nDate of Birth: {dob}\nAge: {age}\nLeague of Legends ID: {lol_id}\nSteam Link: {steam_link}\nSecurity Question #1: {security_question1}\nSecurity Question #2: {security_question2}\nUsername: {username}\nPassword: {password}"

        # Publish the data to RabbitMQ
        channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=registration_data)

        return 'Registration data sent to RabbitMQ'

if __name__ == '__main__':
    app.run(debug=True)
