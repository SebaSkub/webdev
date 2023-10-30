from flask import Flask, request
import pika
import json

app = Flask(__name__)

# Configure RabbitMQ connection parameters
rabbitmq_host = 'sar490'  # Update with your RabbitMQ server host
rabbitmq_port = 5672
rabbitmq_user = 'it490'
rabbitmq_password = 'it490'
rabbitmq_queue = 'userRegister_FTOB'

# Define a function to send data to RabbitMQ
def send_to_rabbitmq(data):
    credentials = PikaCredentials(username = rabbitmq_user, password = rabbitmq_password)
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials))
    channel = connection.channel()
    
    # Declare a queue for registration data
    channel.queue_declare(queue=rabbitmq_queue)
    
    # Send the data as JSON to the RabbitMQ queue
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=json.dumps(data))
    
    connection.close()

# Define a route to handle the form submission

@app.route("/it490/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
    # Get form data
    email = request.form.get('email')
    first_name = request.form.get('first')
    last_name = request.form.get('last')
    username = request.form.get('user')
    password = request.form.get('pass')
    
    # New registration information
    dob = request.form.get('DOB')
    age = request.form.get('age')
    lol_id = request.form.get('lolID')
    steam_link = request.form.get('steamLink')
    sec_question_1 = request.form.get('secQuest1')
    sec_question_2 = request.form.get('secQuest2')

    # Create a dictionary with form data
    data = {
        'type': 'register',
        'email': email,
        'first': first_name,
        'last': last_name,
        # Include the new registration information
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

        # Print form data to the console (optional)
        print(f"Email: {email}")
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Username: {username}")
        print(f"Password: {password}")
        
        # Print new registration information (optional)
        print(f"Date of Birth: {dob}")
        print(f"Age: {age}")
        print(f"League of Legends ID: {lol_id}")
        print(f"Steam Link: {steam_link}")
        print(f"Security Question #1: {sec_question_1}")
        print(f"Security Question #2: {sec_question_2}")

        # You can process and store the data as needed here

        # Redirect to a success page or handle the response as needed
        return "User registration submitted successfully."
    except Exception as e:
        # Handle any exceptions that may occur during RabbitMQ interaction
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run()
