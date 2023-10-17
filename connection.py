import pika

# Establish a connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='my_queue')

# Publish a message to the queue
message_body = "Hello, RabbitMQ!"
channel.basic_publish(exchange='', routing_key='my_queue', body=message_body)

# Close the connection
connection.close()
