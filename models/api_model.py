import os
import requests
from dotenv import load_dotenv
from .token_model import TokenStorage
import sys 


# Determine the base path for the .env file
if getattr(sys, 'frozen', False):
    # If running as a bundled executable, use the executable's directory
    base_path = sys._MEIPASS  # This is the temporary folder where PyInstaller unpacks files
else:
    # Otherwise, use the current file's directory
    base_path = os.path.dirname(__file__)

# Load environment variables from the .env file
load_dotenv(os.path.join(base_path, '.env'))

# Retrieve API URLs from environment variables
API_URL = "http://192.168.23.20:3001/popcen"
LOGIN_URL = "http://192.168.23.20:3001/user/login"
API_COUNT_URL = "http://192.168.23.20:3001/popcenCount"
SIGNUP_URL = "http://192.168.23.20:3001/user/register" # Moved here for better visibility


# Ensure required environment variables are defined
if not API_URL:
    raise ValueError("API_URL environment variable is not set.")
if not LOGIN_URL:
    raise ValueError("LOGIN_URL environment variable is not set.")
if not API_COUNT_URL:
    raise ValueError("API_COUNT_URL environment variable is not set.")
if not SIGNUP_URL:
    raise ValueError("SIGNUP_URL environment variable is not set.")

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
            print(f"Response data: {response_data}")  # Debugging line
            raise ValueError("Authentication token not found in the response.")

        # Store the token
        TokenStorage.set_token(token)

        return token

    except requests.ConnectionError:
        raise RuntimeError("Failed to connect to the API.")
    except requests.Timeout:
        raise RuntimeError("Request timed out.")
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to log in: {str(e)}")
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

    try:
        response = requests.post(SIGNUP_URL, json=json_body, headers=headers)
        response.raise_for_status()  # Raises an exception for 4xx and 5xx responses

    except requests.RequestException as e:
        # Print the error response content if available
        if e.response is not None:
            print(f"Error response content: {e.response.content.decode()}")
        else:
            print("No response content available.")
        raise RuntimeError(f"Failed to sign up: {str(e)}")
