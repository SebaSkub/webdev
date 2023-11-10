<?php
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

require_once __DIR__ . '/vendor/autoload.php'; // Include the Composer autoloader

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $rabbitmq_host = 'sars490'; // Update with your RabbitMQ server host
    $rabbitmq_port = 5672;
    $rabbitmq_user = 'it490';
    $rabbitmq_password = 'it490';
    $rabbitmq_queue = 'tst';

    $connection = new AMQPStreamConnection($rabbitmq_host, $rabbitmq_port, $rabbitmq_user, $rabbitmq_password);
    $channel = $connection->channel();
    $channel->queue_declare($rabbitmq_queue, false, true, false, false);

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

    $msg = new AMQPMessage($registration_data);
    $channel->basic_publish($msg, '', $rabbitmq_queue);

    // Close the connection
    $channel->close();
    $connection->close();

    // Redirect to the login page after successful registration
    header("Location: /it490/login_pg.php");
    exit;
}
?>
