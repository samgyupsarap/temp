import os
import requests
from dotenv import load_dotenv
from .token_model import TokenStorage

# Load environment variables from the .env file
load_dotenv()

# Retrieve API URLs from environment variables
API_URL = os.getenv('API_URL')
LOGIN_URL = os.getenv('LOGIN_URL')
API_COUNT_URL = os.getenv('API_COUNT_URL')

# Ensure required environment variables are defined
if not API_URL:
    raise ValueError("API_URL environment variable is not set.")
if not LOGIN_URL:
    raise ValueError("LOGIN_URL environment variable is not set.")
if not API_COUNT_URL:
    raise ValueError("API_COUNT_URL environment variable is not set.")

def login(username, password):
    """Log in to the API and retrieve the authentication token."""
    headers = {
        "Content-Type": "application/json"
    }
    json_body = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(LOGIN_URL, json=json_body, headers=headers)
        response.raise_for_status()  # Raises an exception if the request failed

        # Assuming the API returns a JSON object with the token
        response_data = response.json()
        token = response_data.get("token")  # Replace "token" with the actual key if different

        if not token:
            raise ValueError("Authentication token not found in the response.")

        # Store the token
        TokenStorage.set_token(token)

        return token

    except requests.RequestException as e:
<<<<<<< HEAD
        raise RuntimeError(f"Failed to log in")
=======
        raise RuntimeError(f"Enter Correct Username and Password")
>>>>>>> 1dfa2a46a2a058e6e268ce24682018c1b2045ab1
    except ValueError as ve:
        raise RuntimeError(str(ve))

def signup(username, password):
    """Register a new user with the API."""
    headers = {
        "Content-Type": "application/json"
    }
    json_body = {
        "username": username,
        "password": password
    }

    SIGNUP_URL = os.getenv('SIGNUP_URL')

    try:
        response = requests.post(SIGNUP_URL, json=json_body, headers=headers)
        response.raise_for_status()  # Raises an exception for 4xx and 5xx responses

    except requests.RequestException as e:
        # Print the error response content if available
        if e.response is not None:
            print(f"Error response content: {e.response.content.decode()}")
        else:
            print("No response content available.")
        raise RuntimeError(f"Failed to sign up")
