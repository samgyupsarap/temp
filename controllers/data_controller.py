import requests
from tkinter import messagebox
from utils.file_utils import save_data_to_file, create_folder_if_not_exists
from models.api_model import API_URL

def fetch_data(caseid_pattern, batchno):
    """Fetch data from the API based on caseidPattern and batchno."""
    url = f"{API_URL}?caseidPattern={caseid_pattern}&batchno={batchno}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception if the request failed
        data = response.json()
        return data
    except requests.RequestException as e:
        messagebox.showerror("API Error", f"Failed to fetch data: {e}")
        return None

def process_batches(folder_path, caseid_pattern):
    batch_no = 1
    while True:
        api_data = fetch_data(caseid_pattern, batch_no)
        
        if not api_data:
            # No more data available
            break
        
        # Create the Batch folder inside the CaseID folder
        subfolder_name = f"Batch_{batch_no}"
        batch_folder_path = create_folder_if_not_exists(folder_path, subfolder_name)
        
        # Save API data to text file
        save_data_to_file(batch_folder_path, batch_no, api_data)
        
        batch_no += 1
