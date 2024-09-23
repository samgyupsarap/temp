import requests
from tkinter import messagebox
from utils.file_utils import save_data_to_file, create_folder_if_not_exists, copy_from_copyfolder
from models.api_model import API_URL
from models.token_model import TokenStorage
import threading
import customtkinter as ctk

def fetch_data(caseid_pattern, batchno, progress_label, records_count):
    """Fetch data from the API and update the progress label."""
    token = TokenStorage.get_token()
    url = f"{API_URL}?caseidPattern={caseid_pattern}&batchno={batchno}&limit={records_count}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if not data.get('results'):
            print(f"No results found for Batch {batchno}.")

        return data
    except requests.RequestException as e:
        messagebox.showerror("API Error", f"Failed to fetch data: {e}")
        return None

def process_batches(folder_path, caseid_pattern, num_batches, records_count):
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

        for batch_no in range(1, num_batches + 1):
            # Update the progress label and bar
            progress_label.configure(text=f"Fetching data for Batch {batch_no}/{num_batches}")
            progress_bar.set(batch_no / num_batches)  # Update progress bar based on batch progress
            progress_window.update()  # Refresh the window to show changes

            api_data = fetch_data(caseid_pattern, batch_no, progress_label, records_count)

            if not api_data or not api_data.get('results'):
                break

            # Create the Batch folder inside the CaseID folder
            subfolder_name = f"{caseid_pattern}_Batch_{batch_no}"
            batch_folder_path, original_folder_path = create_folder_if_not_exists(folder_path, subfolder_name)

            # Save API data to text file
            save_data_to_file(batch_folder_path, caseid_pattern, batch_no, api_data, original_folder_path)

            # Copy files and folders from CopyFolder to the batch folder
            copy_from_copyfolder(batch_folder_path, caseid_pattern, batch_no)

        # Close the progress window when done
        progress_label.configure(text="Completed!")
        progress_bar.set(1)
        progress_window.update()
        progress_window.after(2000, progress_window.destroy)  # Close the window after a delay

    # Start fetching batches in a separate thread
    threading.Thread(target=fetch_batches).start()
