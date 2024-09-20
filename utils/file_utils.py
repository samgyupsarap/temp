import shutil
import os

def create_folder_if_not_exists(parent_folder, folder_name):
    """Create a folder if it doesn't exist, and append (new) if a folder with the same name already exists."""
    batch_folder_path = os.path.join(parent_folder, folder_name)
    original_folder_path = batch_folder_path
    
    count = 1
    while os.path.exists(batch_folder_path):
        batch_folder_path = os.path.join(parent_folder, f"{folder_name} ({count})")
        count += 1

    os.makedirs(batch_folder_path, exist_ok=True)
    return batch_folder_path, original_folder_path

def save_data_to_file(folder_path, caseid_pattern, batch_no, api_data, original_folder_path):
    """Save case IDs to a text file and update the extractData.pff."""
    txt_file_name = f"{caseid_pattern}_Batch_{batch_no}.txt"
    txt_file_path = os.path.join(folder_path, txt_file_name)

    try:
        results = api_data.get('results', [])
        with open(txt_file_path, "w") as file:
            for item in results:
                if isinstance(item, dict) and 'caseid' in item:
                    file.write(f"{item['caseid']}\n")

    except Exception as e:
        print(f"Error saving case IDs to file: {e}")

    path_file_path = os.path.join(folder_path, "batch_path.txt")
    try:
        with open(path_file_path, "w") as path_file:
            path_file.write(f"{os.path.abspath(txt_file_path)}")
    except Exception as e:
        print(f"Error saving batch path to file: {e}")

def copy_from_copyfolder(batch_folder_path, caseid_pattern, batch_no):
    """Copy files from CopyFolder to the batch folder and modify extractData.pff if it exists."""
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

    # Check if extractData.pff exists and update it
    pff_file_path = os.path.join(batch_folder_path, "extractData.pff")
    if os.path.exists(pff_file_path):
        update_extract_data(pff_file_path, caseid_pattern, batch_no)
        run_pff_file(pff_file_path)  # Automatically run the .pff file after modification


def update_extract_data(pff_file_path, caseid_pattern, batch_no):
    """Update extractData.pff to include the complete path for INPUT_FILE."""
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
        print(f"Error updating extractData.pff: {e}")


def run_pff_file(pff_file_path):
    """Automatically run the .pff file."""
    try:
        os.startfile(pff_file_path)  # This will attempt to open the .pff file with its associated application

    except Exception as e:
        print(f"Error running {pff_file_path}: {e}")
