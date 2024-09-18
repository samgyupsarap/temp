import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve API_URL from environment variables
API_URL = os.getenv('API_URL')
