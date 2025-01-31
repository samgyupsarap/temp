import shutil
import os
import customtkinter as ctk
import subprocess
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor

def create_folder_if_not_exists(parent_folder, folder_name):
    """Create a folder if it doesn't exist, and append (new) if a folder with the same name already exists."""
    os.makedirs(parent_folder, exist_ok=True)
    
    batch_folder_path = os.path.join(parent_folder, folder_name)
    
    # Use a count to create unique folder names if necessary
    count = 1
    while os.path.exists(batch_folder_path):
        batch_folder_path = os.path.join(parent_folder, f"{folder_name} ({count})")
        count += 1

    os.makedirs(batch_folder_path, exist_ok=True)  # Create the final batch folder
    return batch_folder_path

def save_data_to_file(folder_path, caseid_pattern, batch_no, case_ids):
    """Save GeoIDs IDs to a text file."""
    txt_file_name = f"{caseid_pattern}_Batch_{batch_no}.txt"
    txt_file_path = os.path.join(folder_path, txt_file_name)

    try:
        with open(txt_file_path, "w") as file:
            for case_id in case_ids:
                file.write(f"{case_id}\n")

        # Save the path of the text file
        path_file_path = os.path.join(folder_path, "batch_path.txt")
        with open(path_file_path, "w") as path_file:
            path_file.write(f"{os.path.abspath(txt_file_path)}")

    except Exception as e:
        print(f"Error saving GeoIDs to file: {e}")

def copy_from_copyfolder(batch_folder_path, caseid_pattern, batch_no):
    """Copy files from CopyFolder to the batch folder and modify download.pff if it exists."""
    copy_folder = os.path.join(os.path.dirname(__file__), '..', 'CopyFolder')

    if not os.path.exists(copy_folder):
        print(f"CopyFolder does not exist at {copy_folder}")
        return

    # Copy all files and folders from CopyFolder to batch folder
    for item in os.listdir(copy_folder):
        s = os.path.join(copy_folder, item)
        d = os.path.join(batch_folder_path, item)

        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    # Check if download.pff exists and update it
    pff_file_path = os.path.join(batch_folder_path, "download.pff")
    if os.path.exists(pff_file_path):
        update_download_data(pff_file_path, caseid_pattern, batch_no)

    # Optionally, open the .pff file after completing the batch
    autorun_pff(pff_file_path)

def fetch_batches(main_batch_folder, caseid_pattern, all_caseids, records_per_batch, total_records):
    """Process all batches and update the progress."""
    num_batches = (total_records + records_per_batch - 1) // records_per_batch  # Calculate number of batches

    # Create a progress window
    progress_window = ctk.CTkToplevel()
    progress_window.title("Fetching Data")
    progress_window.geometry("300x150")

    progress_label = ctk.CTkLabel(progress_window, text="Starting batch processing...")
    progress_label.pack(pady=10)

    progress_bar = ctk.CTkProgressBar(progress_window, width=250)
    progress_bar.pack(pady=10)
    progress_bar.set(0)

    def save_batch(batch_no):
        start_index = (batch_no - 1) * records_per_batch
        end_index = min(start_index + records_per_batch, total_records)
        batch_caseids = all_caseids[start_index:end_index]

        # Create the Batch folder inside the main batch directory
        subfolder_name = f"{caseid_pattern}_Batch_{batch_no}"
        batch_folder_path = create_folder_if_not_exists(main_batch_folder, subfolder_name)

        # Save case IDs to a text file
        save_data_to_file(batch_folder_path, caseid_pattern, batch_no, batch_caseids)

        # Copy files from CopyFolder and update .pff if needed
        copy_from_copyfolder(batch_folder_path, caseid_pattern, batch_no)

        # Update progress
        progress_label.configure(text=f"Completed Batch {batch_no}/{num_batches}")
        progress_bar.set(batch_no / num_batches)
        progress_window.update()

    # Run the batch processing using a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=5) as executor:
        for batch_no in range(1, num_batches + 1):
            executor.submit(save_batch, batch_no)

    # Close the progress window once all batches are completed
    progress_label.configure(text="All batches completed!")
    progress_bar.set(1)
    progress_window.update()
    progress_window.after(2000, progress_window.destroy)

    # After all batches are processed, open the .pff file from the first batch
    pff_file_path = os.path.join(main_batch_folder, f"{caseid_pattern}_Batch_1", "download.pff")
    if os.path.exists(pff_file_path):
        autorun_pff(pff_file_path)

def update_download_data(pff_file_path, caseid_pattern, batch_no):
    """Update download.pff to include the complete path for INPUT_FILE."""
    txt_file_name = f"{caseid_pattern}_Batch_{batch_no}.txt"
    input_file_path = os.path.abspath(os.path.join(os.path.dirname(pff_file_path), txt_file_name))

    try:
        with open(pff_file_path, "r") as file:
            lines = file.readlines()

        # Write back the modified lines
        with open(pff_file_path, "w") as file:
            for line in lines:
                if line.startswith("INPUT_FILE="):
                    line = f"INPUT_FILE={input_file_path}\n"
                file.write(line)

    except Exception as e:
        print(f"Error updating download.pff: {e}")

def autorun_pff(pff_file_path):
    """Open the .pff file with the default associated application."""
    try:
        if os.name == 'posix':  # For macOS/Linux
            subprocess.run(['open', pff_file_path], check=True)
        elif os.name == 'nt':  # For Windows
            os.startfile(pff_file_path)  # startfile is used in Windows to open files with their associated app
        else:
            messagebox.showerror("Unsupported OS", "This feature is not supported on your operating system.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open the .pff file: {e}")

# Call the fetch_batches function somewhere in your code with appropriate arguments
