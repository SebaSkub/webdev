// Include the fetch library or use a polyfill if needed
// Example using 'node-fetch' in a Node.js environment:
const fetch = require('node-fetch');

// Assuming you have defined a function to perform a redirect
function redirect(message, destination, delay) {
    console.log(message);
    setTimeout(() => {
        window.location.href = destination;
    }, delay * 1000);
}

// Assuming you have defined the 'getSessionValue' function to get session values
// Replace this with your actual implementation for managing sessions

// Set the URL of your server
const serverUrl = 'http://10.198.120.114:8080';

// Data to send in the POST request
const data = {
    type: 'register',
    email: getSessionValue('email'), // Replace with your session data retrieval
    first: getSessionValue('first'),
    last: getSessionValue('last'),
    user: getSessionValue('user'),
    pass: getSessionValue('pass')
};

// Configure the fetch request
fetch(`${serverUrl}/register`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
})
.then(response => response.json()) // Assuming the response is in JSON format
.then(responseData => {
    if (responseData.message === 'User Created!') {
        // Handle success
        // Set session variables or redirect as needed
        redirect('User successfully registered. Redirecting to build dietary profile.', 'buildprofile.html', 3);
    } else if (responseData.message === 'Duplicate') {
        // Handle duplicate email case
        redirect('Email already in use. Please use a different email or try logging in using that email.', 'register.html', 3);
    } else {
        // Handle other response cases
    }
})
.catch(error => {
    // Handle network errors or other issues
    console.error('Error:', error);
});
