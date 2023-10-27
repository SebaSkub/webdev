// Function to handle redirection (define your own redirection logic)
function redirect(message, destination, delay) {
    console.log(message);
    // Implement your redirection logic here
    setTimeout(() => {
        window.location.href = destination;
    }, delay * 1000);
}

// Function to get session values (replace with your actual implementation)
function get_session_value(key) {
    // Implement your session data retrieval logic here
    return null;
}

// Set the URL of your server
const serverUrl = 'http://10.198.120.114:7007';

// Data to send in the POST request
const data = {
    type: 'register',
    email: get_session_value('email'),  // Replace with your session data retrieval
    first: get_session_value('first'),
    last: get_session_value('last'),
    user: get_session_value('user'),
    pass: get_session_value('pass')
};

// Configure the POST request
fetch(`${serverUrl}/register`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(responseData => {
    if (responseData.message === 'User Created!') {
        // Handle success
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
