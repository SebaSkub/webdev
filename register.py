from flask import Flask, request, render_template
import pika

app = Flask(__name__)

# RabbitMQ connection parameters
RABBITMQ_HOST = '10.198.120.114'  # Update with your RabbitMQ server host
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'it490'
RABBITMQ_PASSWORD = 'it490'
RABBITMQ_QUEUE = 'userRegister_FTOB'

@app.route('/it490/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_data = request.form

        email = form_data.get('email')
        first = form_data.get('first')
        last = form_data.get('last')
        DOB = form_data.get('DOB')
        age = form_data.get('age')
        lolID = form_data.get('lolID')
        steamLink = form_data.get('steamLink')
        secQuest1 = form_data.get('secQuest1')
        secQuest2 = form_data.get('secQuest2')
        user = form_data.get('user')
        passw = form_data.get('pass')

        # Format the data as a message
        message = f"Email: {email}, First Name: {first}, Last Name: {last}, DOB: {DOB}, Age: {age}, LOL ID: {lolID}, Steam Link: {steamLink}, Security Question #1: {secQuest1}, Security Question #2: {secQuest2}, Username: {user}, Password: {passw}"

        # Publish the message to RabbitMQ
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=credentials
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE)
        channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=message)
        connection.close()

        return "Registration successful!"

    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7007)
