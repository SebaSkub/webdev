import pika
import json

# RabbitMQ connection parameters
RABBITMQ_HOST = '10.198.120.114'  # Update with your RabbitMQ server host
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'it490'
RABBITMQ_PASSWORD = 'it490'
RABBITMQ_QUEUE = 'userRegister_FTOB'

app = Flask(__name)

# Establish a connection to RabbitMQ
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    credentials=credentials
))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue=RABBITMQ_QUEUE)

def send_to_rabbitmq(data):
    try:
        # Publish the user registration data to the RabbitMQ queue
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(data),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make the message persistent
            )
        )
        print(" [x] Sent user data to RabbitMQ")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example endpoint to handle the user registration
@app.route('/register', methods=['POST'])
def register():
    user_data = request.json  # Assuming the data is received as JSON
    # You can add data validation and additional processing here

    # Send user data to RabbitMQ
    send_to_rabbitmq(user_data)

    return "Registration successful"

if __name__ == '__main__':
    app.run()
