# Import necessary libraries
from flask import Flask, request, render_template
import pika
from pika.credentials import PlainCredentials as PikaCredentials

app = Flask(__name)

# Configure RabbitMQ connection parameters
rabbitmq_host = 'sars490'  # Update with your RabbitMQ server host
rabbitmq_port = 5672
rabbitmq_user = 'it490'
rabbitmq_password = 'it490'
rabbitmq_queue = 'userRegister_FTOB'

# Define a function to send data to RabbitMQ
def send_to_rabbitmq(data):
    credentials = PikaCredentials(username=rabbitmq_user, password=rabbitmq_password)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials))
    channel = connection.channel()

    # Declare a queue for registration data
    channel.queue_declare(queue=rabbitmq_queue)

    # Convert data to a message (e.g., JSON)
    message = json.dumps(data)  # You may want to use JSON or another format for your data

    # Send the data to the RabbitMQ queue
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=message)

    connection.close()

# Define a route to handle the form submission
@app.route("/it490/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        # Get form data
        email = request.form.get('email')
        first_name = request.form.get('first')
        last_name = request.form.get('last')

        # New registration information
        dob = request.form.get('DOB')
        age = request.form.get('age')
        lol_id = request.form.get('lolID')
        steam_link = request.form.get('steamLink')
        sec_question_1 = request.form.get('secQuest1')
        sec_question_2 = request.form.get('secQuest2')
        username = request.form.get('user')
        password = request.form.get('pass')

        # Create a dictionary with form data
        data = {
            'type': 'register',
            'email': email,
            'first': first_name,
            'last': last_name,
            'DOB': dob,
            'age': age,
            'lolID': lol_id,
            'steamLink': steam_link,
            'secQuest1': sec_question_1,
            'secQuest2': sec_question_2,
            'user': username,
            'pass': password
        }

        try:
            # Send data to RabbitMQ
            send_to_rabbitmq(data)

            # You can process and store the data as needed here

            # Redirect to a success page or handle the response as needed
            return "User registration submitted successfully."
        except Exception as e:
            # Handle any exceptions that may occur during RabbitMQ interaction
            return f"Error: {str(e)}"

    # For GET requests, display the registration form
    return render_template('it490/register.html')

if __name__ == '__main__':
    app.run(debug=True)
