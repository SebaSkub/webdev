import requests

# Function to redirect (you can define your own redirection logic)
def redirect(message, destination, delay):
    print(message)
    # Implement your redirection logic here

# Function to get session values (replace with your actual implementation)
def get_session_value(key):
    # Implement your session data retrieval logic here
    return None

# Set the URL of your server
server_url = 'http://10.198.120.114:7007'

# Data to send in the POST request
data = {
    'type': 'register',
    'email': get_session_value('email'),  # Replace with your session data retrieval
    'first': get_session_value('first'),
    'last': get_session_value('last'),
    'user': get_session_value('user'),
    'pass': get_session_value('pass')
}

# Configure the POST request
response = requests.post(f'{server_url}/register', json=data)

# Handle the response
if response.status_code == 200:
    response_data = response.json()
    if response_data['message'] == 'User Created!':
        # Handle success
        # Set session variables or redirect as needed
        redirect('User successfully registered. Redirecting to build dietary profile.', 'buildprofile.html', 3)
    elif response_data['message'] == 'Duplicate':
        # Handle duplicate email case
        redirect('Email already in use. Please use a different email or try logging in using that email.', 'register.html', 3)
    else:
        # Handle other response cases
else:
    # Handle network errors or other issues
    print(f'Error: {response.status_code}')
