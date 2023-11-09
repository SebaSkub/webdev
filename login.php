<?php
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

require_once 'composer.json'; // Include the Composer autoloader

$rabbitmq_host = 'it490mjt'; // Update with your RabbitMQ server host
$rabbitmq_port = 5672;
$rabbitmq_user = 'it490';
$rabbitmq_password = 'it490';
$rabbitmq_queue = 'test'; // Replace with the name of your login queue

function send_to_rabbitmq($data) {
    global $rabbitmq_host, $rabbitmq_port, $rabbitmq_user, $rabbitmq_password, $rabbitmq_queue;

    try {
        // Initialize a connection to RabbitMQ
        $connection = new AMQPStreamConnection($rabbitmq_host, $rabbitmq_port, $rabbitmq_user, $rabbitmq_password);
        $channel = $connection->channel();
        $channel->queue_declare($rabbitmq_queue, false, true, false, false);

        // Send the data to RabbitMQ in the desired format
        $message = new AMQPMessage($data);
        $channel->basic_publish($message, '', $rabbitmq_queue);

        // Close the connection
        $channel->close();
        $connection->close();
    } catch (Exception $e) {
        // Handle exceptions if the connection or message sending fails
        echo "Failed to send data to RabbitMQ: " . $e->getMessage();
    }
}

// Your login route
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    try {
        $username = $_POST['username'];
        $password = $_POST['password'];

        // Assuming valid login, send data to RabbitMQ in the desired format
        $login_data = "$username,$password";
        send_to_rabbitmq($login_data);
        header("Location: /it490/landing.html");
        exit;
    } catch (Exception $e) {
        echo "Login failed";
        http_response_code(400);
        exit;
    }
}
?>
