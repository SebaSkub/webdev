document.getElementById('registration-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const registrationData = {
        username: username,
        email: email,
        password: password,
        page: 'registration'
    };

    // Make an HTTP POST request to the server to send registration data
    fetch('/registration', {
        method: 'POST',
        body: JSON.stringify(registrationData),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    });
});
