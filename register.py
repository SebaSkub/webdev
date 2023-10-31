import pika
import cgi
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

# RabbitMQ connection parameters
RABBITMQ_HOST = '10.198.120.114'  # Update with your RabbitMQ server host
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'it490'
RABBITMQ_PASSWORD = 'it490'
RABBITMQ_QUEUE = 'userRegister_FTOB'

# Define a class to handle HTTP requests
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        # Extract form data
        email = form.getvalue('email')
        first = form.getvalue('first')
        last = form.getvalue('last')
        DOB = form.getvalue('DOB')
        age = form.getvalue('age')
        lolID = form.getvalue('lolID')
        steamLink = form.getvalue('steamLink')
        secQuest1 = form.getvalue('secQuest1')
        secQuest2 = form.getvalue('secQuest2')
        user = form.getvalue('user')
        passw = form.getvalue('pass')

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

        # Send a response to the browser
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Registration successful!')

if __name__ == '__main__':
    try:
        server = HTTPServer(('', 80), RequestHandler)
        print('Started HTTP server')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down the server')
        server.socket.close()
