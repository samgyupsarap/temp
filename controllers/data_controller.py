import requests
from tkinter import messagebox, filedialog
from utils.file_utils import save_data_to_file, create_folder_if_not_exists, copy_from_copyfolder
from models.api_model import API_URL, API_COUNT_URL  # Ensure you have a count URL for total records
from models.token_model import TokenStorage
import threading
import customtkinter as ctk
from concurrent.futures import ThreadPoolExecutor
import os
import time

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
        
        total_records = data.get('count', 0)
        return total_records if isinstance(total_records, int) else total_records.get('count', 0)
    except requests.RequestException as e:
        messagebox.showerror("API Error", "Failed to fetch total records")
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
        caseids = [result['caseids'] for result in data.get('results', [])]

        return caseids  # Return only caseid list
    except requests.RequestException as e:
        messagebox.showerror("API Error", "Failed to fetch data")
        return None

def process_batches(parent_folder_path, caseid_pattern, records_per_batch, progress_label, progress_bar, progress_window):
    """Process batches based on the number of records per batch and total records in the API."""
    main_batch_folder = create_folder_if_not_exists(parent_folder_path, caseid_pattern)
    total_records = get_total_records(caseid_pattern)

    if total_records == 0:
        messagebox.showerror("No Data", "No records found for the given GeoIDs pattern.")
        progress_window.destroy()
        return

    all_caseids = fetch_all_data(caseid_pattern, total_records)

    if not all_caseids:
        messagebox.showerror("No Data", "No records found for the given GeoIDs pattern.")
        progress_window.destroy()
        return

    total_records = len(all_caseids)
    num_batches = (total_records + records_per_batch - 1) // records_per_batch  # Ceiling division

    def save_batch(batch_no):
        start_index = (batch_no - 1) * records_per_batch
        end_index = min(start_index + records_per_batch, total_records)
        batch_caseids = all_caseids[start_index:end_index]

        subfolder_name = f"{caseid_pattern}_Batch_{batch_no}"
        batch_folder_path = create_folder_if_not_exists(main_batch_folder, subfolder_name)

        save_data_to_file(batch_folder_path, caseid_pattern, batch_no, batch_caseids)
        copy_from_copyfolder(batch_folder_path, caseid_pattern, batch_no)

        progress_label.configure(text=f"Completed Batch {batch_no}/{num_batches}")
        progress_bar.set(batch_no / num_batches)
        progress_window.update()

    with ThreadPoolExecutor(max_workers=10) as executor:
        for batch_no in range(1, num_batches + 1):
            executor.submit(save_batch, batch_no)
            time.sleep(0.5)  # Small delay to avoid crashing

    progress_label.configure(text="All batches completed!")
    progress_bar.set(1)
    progress_window.update()
    progress_window.after(2000, progress_window.destroy)

def handle_submit(caseid_pattern, records_per_batch):
    """Handle the submit logic from the main view."""
    folder_path = filedialog.askdirectory(title="Select Parent Directory")

    if not folder_path:
        messagebox.showwarning("No Directory Selected", "Please select a directory.")
        return

    total_records = get_total_records(caseid_pattern)

    if total_records == 0:
        messagebox.showerror("No Data", "No records found for the given GeoIDs pattern.")
        return

    num_batches = (total_records + records_per_batch - 1) // records_per_batch

    if num_batches > 30:
        messagebox.showwarning(
            "Too Many Batches",
            f"The number of batches ({num_batches}) exceeds the allowed limit of 30. "
            "Please increase the number of records per batch and try again."
        )
        return

    confirm_message = f"This operation will generate {num_batches} batches, each with up to {records_per_batch} records.\n\nDo you want to proceed?"
    confirm = messagebox.askyesno("Confirm Batch Generation", confirm_message)

    if not confirm:
        return

    progress_window = ctk.CTkToplevel()
    progress_window.title("Processing Batches")
    progress_window.geometry("300x150")

    progress_label = ctk.CTkLabel(progress_window, text="Starting batch processing...")
    progress_label.pack(pady=10)

    progress_bar = ctk.CTkProgressBar(progress_window, width=250)
    progress_bar.pack(pady=10)
    progress_bar.set(0)

    threading.Thread(target=lambda: process_batches(folder_path, caseid_pattern, records_per_batch, progress_label, progress_bar, progress_window)).start()
