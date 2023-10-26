const express = require('express');
const bodyParser = require('body-parser');
const amqp = require('amqplib/callback_api');

const app = express();
const PORT = 3000;

app.use(bodyParser.urlencoded({ extended: true }));

// RabbitMQ connection
const rabbitMqUrl = 'amqp://localhost';
const queueName = 'registration_queue';

amqp.connect(rabbitMqUrl, (error0, connection) => {
    if (error0) throw error0;

    connection.createChannel((error1, channel) => {
        if (error1) throw error1;

        channel.assertQueue(queueName, {
            durable: false
        });

        // Handling registration data
        app.post('/register', (req, res) => {
            const { username, password } = req.body;

            // Send registration data to RabbitMQ queue
            channel.sendToQueue(queueName, Buffer.from(`Registration: ${username}, ${password}`));

            res.send('Registration data sent to RabbitMQ.');
        });

        // Handling login data
        app.post('/login', (req, res) => {
            const { username, password } = req.body;

            // Send login data to RabbitMQ queue
            channel.sendToQueue(queueName, Buffer.from(`Login: ${username}, ${password}`));

            res.send('Login data sent to RabbitMQ.');
        });
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
