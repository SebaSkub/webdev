document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const username = document.getElementById('user').value;
    const password = document.getElementById('pass').value;

    const loginData = {
        username: user,
        password: pass,
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
