<?php
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

require_once 'vendor/autoload.php'; // Include the Composer autoloader

$rabbitmq_host = 'it490mjt'; // Update with your RabbitMQ server host
$rabbitmq_port = 5672;
$rabbitmq_user = 'it490';
$rabbitmq_password = 'it490';
$rabbitmq_queue = 'test';

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

// Handle the form submission
if ('REQUEST_METHOD'] === 'POST') {
    try {
        // Collect form data
        $first_name = $_POST['firstName'];
        $last_name = $_POST['lastName'];
        $dob = $_POST['dob'];
        $age = $_POST['age'];
        $lol_id = $_POST['lolId'];
        $steam_link = $_POST['steamLink'];
        $security_question1 = $_POST['securityQuestion1'];
        $security_question2 = $_POST['securityQuestion2'];
        $username = $_POST['username'];
        $password = $_POST['password'];

        // Prepare the data as a comma-separated string
        $registration_data = "$first_name,$last_name,$dob,$age,$lol_id,$steam_link,$security_question1,$security_question2,$username,$password";

        // Use the send_to_rabbitmq function to publish the data to RabbitMQ
        send_to_rabbitmq($registration_data);

        // Redirect to the login page after successful registration
        header("Location: /it490/login.html");
        exit;
    } catch (Exception $e) {
        echo "Registration failed";
        http_response_code(400);
        exit;
    }
}
?>
