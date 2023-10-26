document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const loginData = {
        username: username,
        password: password,
        page: 'login'
    };

    // Make an HTTP POST request to the server to send login data
    fetch('/login', {
        method: 'POST',
        body: JSON.stringify(loginData),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    });
});
