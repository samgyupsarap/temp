import requests
from tkinter import messagebox
from utils.file_utils import save_data_to_file, create_folder_if_not_exists, copy_from_copyfolder
from models.api_model import API_URL, API_COUNT_URL  # Ensure you have a count URL for total records
from models.token_model import TokenStorage
import threading
import customtkinter as ctk
from concurrent.futures import ThreadPoolExecutor

def get_total_records(caseid_pattern):
    """Fetch the total number of records available from the custom API."""
    token = TokenStorage.get_token()
    url = f"{API_COUNT_URL}?caseidPattern={caseid_pattern}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Extract the count correctly
        total_records = data.get('count', 0)
        return total_records if isinstance(total_records, int) else total_records.get('count', 0)
    except requests.RequestException as e:
        messagebox.showerror("API Error", f"Failed to fetch total records: {e}")
        return 0

def fetch_all_data(caseid_pattern, max_limit):
    """Fetch all data from the API based on the caseid_pattern."""
    token = TokenStorage.get_token()
    url = f"{API_URL}?caseidPattern={caseid_pattern}&limit={max_limit}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Extract only caseid from the results
        caseids = [result['caseid'] for result in data.get('results', [])]

        return caseids  # Return only caseid list
    except requests.RequestException as e:
        messagebox.showerror("API Error", f"Failed to fetch data: {e}")
        return None

def process_batches(folder_path, caseid_pattern, records_per_batch):
    """Process batches based on the number of records per batch and total records in the API."""
    
    # Fetch total records count first
    total_records = get_total_records(caseid_pattern)
    
    if total_records == 0:
        messagebox.showerror("No Data", "No records found for the given CaseID pattern.")
        return

    # Now fetch all case IDs with the correct limit
    all_caseids = fetch_all_data(caseid_pattern, total_records)

    if not all_caseids:
        messagebox.showerror("No Data", "No records found for the given CaseID pattern.")
        return

    # Calculate the number of batches needed
    total_records = len(all_caseids)
    num_batches = (total_records + records_per_batch - 1) // records_per_batch  # Ceiling division

    def fetch_batches():
        # Create a progress window
        progress_window = ctk.CTkToplevel()
        progress_window.title("Fetching Data")
        progress_window.geometry("300x150")

        # Progress label
        progress_label = ctk.CTkLabel(progress_window, text="Starting batch processing...")
        progress_label.pack(pady=10)

        # Progress bar
        progress_bar = ctk.CTkProgressBar(progress_window, width=250)
        progress_bar.pack(pady=10)
        progress_bar.set(0)  # Initialize the progress bar to 0

        # Function to handle saving a single batch
        def save_batch(batch_no):
            start_index = (batch_no - 1) * records_per_batch
            end_index = min(start_index + records_per_batch, total_records)
            batch_caseids = all_caseids[start_index:end_index]

            # Create the Batch folder inside the CaseID folder
            subfolder_name = f"{caseid_pattern}_Batch_{batch_no}"
            batch_folder_path = create_folder_if_not_exists(folder_path, subfolder_name)

            # Save API data to a text file (only case IDs)
            save_data_to_file(batch_folder_path, caseid_pattern, batch_no, batch_caseids)

            # Copy files and folders from CopyFolder to the batch folder
            copy_from_copyfolder(batch_folder_path, caseid_pattern, batch_no)

            # Update progress
            progress_label.configure(text=f"Completed Batch {batch_no}/{num_batches}")
            progress_bar.set(batch_no / num_batches)  # Update progress bar
            progress_window.update()  # Refresh the window to show changes

        # Use ThreadPoolExecutor to run batch saving concurrently
        with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust the number of workers as needed
            for batch_no in range(1, num_batches + 1):
                executor.submit(save_batch, batch_no)

        # Close the progress window when done
        progress_label.configure(text="All batches completed!")
        progress_bar.set(1)
        progress_window.update()
        progress_window.after(2000, progress_window.destroy)  # Close the window after a delay

    # Start fetching batches in a separate thread
    threading.Thread(target=fetch_batches).start()
