import pika
from flask import Flask, request, redirect

# RabbitMQ connection parameters
rabbitmq_host = 'sars490'  # Update with your RabbitMQ server host
rabbitmq_port = 5672
rabbitmq_user = 'it490'
rabbitmq_password = 'it490'
rabbitmq_queue = 'userRegister_FTOB'

app = Flask(__name__)

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

        # Prepare the data as a comma-separated string
        registration_data = f"{first_name},{last_name},{dob},{age},{lol_id},{steam_link},{security_question1},{security_question2},{username},{password}"

        # Use the send_to_rabbitmq function to publish the data to RabbitMQ
        send_to_rabbitmq(registration_data)

        # Redirect to the login page after successful registration
        return redirect('/it490/login.html')

if __name__ == '__main__':
    app.run(host='10.198.120.126', port=7007)
