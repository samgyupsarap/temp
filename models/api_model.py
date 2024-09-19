import os
from dotenv import load_dotenv
import requests

# Load environment variables from the .env file
load_dotenv()

# Retrieve API_URL from environment variables
API_URL = os.getenv('API_URL')
LOGIN_URL = os.getenv('LOGIN_URL')
# Ensure API_URL is defined
if not API_URL:
    raise ValueError("API_URL environment variable is not set.")
if not LOGIN_URL:
    raise ValueError("LOGIN_URL environment variable is not set.")

LOGIN_URL = f"{LOGIN_URL}"  # Ensure proper URL formation

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

        return token

    except requests.RequestException as e:
        raise RuntimeError(f"Failed to log in: {e}")
    except ValueError as ve:
        raise RuntimeError(str(ve))
