@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('user')
            password = request.form.get('pass')

            # Validate user's credentials (you can implement your own validation logic here)
            # For example, check if the username and password are correct

            if username == 'example_username' and password == 'example_password':
                # Assuming valid login, send data to RabbitMQ
                login_data = f"{username}, {password}"
                send_to_rabbitmq(login_data)
                # Redirect to the landing page after successful login
                return redirect('/it490/landing.html')

            else:
                return 'Invalid username or password', 401

        except Exception as e:
            return 'Login failed', 400

if __name__ == '__main__':
    app.run()
