import requests
from tkinter import messagebox
from utils.file_utils import save_data_to_file, create_folder_if_not_exists, copy_from_copyfolder
from models.api_model import API_URL
from models.token_model import TokenStorage

def fetch_data(caseid_pattern, batchno):
    """Fetch data from the API based on caseidPattern and batchno."""
    token = TokenStorage.get_token()  # Retrieve the token from storage
    url = f"{API_URL}?caseidPattern={caseid_pattern}&batchno={batchno}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an exception if the request failed
        data = response.json()

        # Debugging: Print the raw response data to verify the format
        print(f"API Response for Batch {batchno}: {data}")

        if not data.get('results'):
            print(f"No results found for Batch {batchno}.")  # Additional debugging info

        return data
    except requests.RequestException as e:
        messagebox.showerror("API Error", f"Failed to fetch data: {e}")
        return None

def process_batches(folder_path, caseid_pattern, num_batches):
    batch_no = 1
    while batch_no <= num_batches:
        api_data = fetch_data(caseid_pattern, batch_no)

        if not api_data or not api_data.get('results'):
            # No more data available or API response is invalid
            break

        # Create the Batch folder inside the CaseID folder
        subfolder_name = f"Batch_{batch_no}"
        batch_folder_path, original_folder_path = create_folder_if_not_exists(folder_path, subfolder_name)

        # Save API data to text file
        save_data_to_file(batch_folder_path, batch_no, api_data, original_folder_path)

        # Copy files and folders from CopyFolder to the batch folder
        copy_from_copyfolder(batch_folder_path)

        batch_no += 1