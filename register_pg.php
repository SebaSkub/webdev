
<!DOCTYPE html>
<html>

<head>
    <title>User Registration</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(to right, #2980b9, #6dd5fa);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .registration-container {
            max-width: 400px;
            background: #333;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
            padding: 20px;
        }

        h2 {
            text-align: center;
            color: #fff;
        }

        form {
            padding: 20px;
        }

        table {
            width: 100%;
        }

        td {
            padding: 10px;
        }

        .top {
            padding-top: 15px;
        }

        input[type="text"],
        input[type="email"],
        input[type="password"],
        input[type="date"],
        input[type="number"],
        input[type="url"] {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #007bff; /* Blue border */
            border-radius: 3px;
            background: #444; /* Dark background */
            color: #fff;
        }

        input[type="submit"] {
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 3px;
            padding: 10px 15px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        input[type="submit"]:hover {
            background-color: #0056b3;
        }

        a {
            text-decoration: none;
            display: block;
            text-align: center;
            margin-top: 10px;
            color: #007bff;
            background: #fff;
            padding: 8px 15px;
            border-radius: 3px;
        }

        a:hover {
            text-decoration: underline;
        }
    </style>
</head>

<body>
    <h2>User Registration</h2>
    <form id="registrationForm" action="register.php" method="POST">
        <div>
            <label for="firstName">First Name:</label>
            <input type="text" id="firstName" name="firstName" required>
        </div>
        <div>
            <label for="lastName">Last Name:</label>
            <input type="text" id="lastName" name="lastName" required>
        </div>
        <div>
            <label for="dob">Date of Birth:</label>
            <input type="date" id="dob" name="dob" required>
        </div>
        <div>
            <label for="age">Age:</label>
            <input type="number" id="age" name="age" required>
        </div>
        <div>
            <label for="lolId">League of Legends ID:</label>
            <input type="text" id="lolId" name="lolId" required>
        </div>
        <div>
            <label for="steamLink">Steam Link:</label>
            <input type="text" id="steamLink" name="steamLink" required>
        </div>
        <div>
            <label for="securityQuestion1">Security Question #1: (Random Word)</label>
            <input type="text" id="securityQuestion1" name="securityQuestion1" required>
        </div>
        <div>
            <label for="securityQuestion2">Security Question #2: (Random PIN)</label>
            <input type="text" id="securityQuestion2" name="securityQuestion2" readonly>
            <button type="button" id="generatePIN">Generate PIN</button>
        </div>

        <h3>Login Information</h3>
        <div>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <div>
            <input type="submit" value="Register">
        </div>
    </form>

    <a href="/login_pg.php">Back to Login</a>

    <script>
        document.getElementById('generatePIN').addEventListener('click', function() {
            const securityQuestion2Input = document.getElementById('securityQuestion2');
            const randomPin = generateRandomPin();
            securityQuestion2Input.value = randomPin;
        });

        function generateRandomPin() {
            return Math.floor(1000 + Math.random() * 9000).toString();
        }
    </script>

</body>
</html>
