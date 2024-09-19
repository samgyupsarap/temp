import shutil
import os

def create_folder_if_not_exists(parent_folder, folder_name):
    """Create a folder if it doesn't exist, and append (new) if a folder with the same name already exists."""
    batch_folder_path = os.path.join(parent_folder, folder_name)
    original_folder_path = batch_folder_path
    
    # Check if the folder exists and adjust the path if necessary
    count = 1
    while os.path.exists(batch_folder_path):
        batch_folder_path = os.path.join(parent_folder, f"{folder_name} (new{count})")
        count += 1

    os.makedirs(batch_folder_path, exist_ok=True)
    return batch_folder_path, original_folder_path


def save_data_to_file(folder_path, batch_no, api_data, original_folder_path):
    """Save only the 'caseid' from the API data to a text file."""
    txt_file_path = os.path.join(folder_path, f"Batch_{batch_no}.txt")

    try:
        # Extract 'results' from API data
        results = api_data.get('results', [])

        # Open the file and write the caseids
        with open(txt_file_path, "w") as file:
            for item in results:
                # Ensure that item is a dictionary and contains 'caseid'
                if isinstance(item, dict) and 'caseid' in item:
                    # Write only the caseid to the file
                    file.write(f"{item['caseid']}\n")
                else:
                    # Log or handle unexpected data
                    print(f"Unexpected item format in results: {item}")

        print(f"Case IDs successfully saved in {txt_file_path}")
    except Exception as e:
        print(f"Error saving case IDs to file: {e}")

    # Create a text file to store the full path of the batch folder without (new) suffix
    path_file_path = os.path.join(folder_path, "batch_path.txt")
    try:
        # Write the original folder path to the path_file_path
        with open(path_file_path, "w") as path_file:
            path_file.write(f"{os.path.abspath(original_folder_path)}")
        print(f"Path successfully saved in {path_file_path}")
    except Exception as e:
        print(f"Error saving batch path to file: {e}")

def copy_from_copyfolder(batch_folder_path):
    """Copy files and folders from CopyFolder to the batch folder."""
    copy_folder = os.path.join(os.path.dirname(__file__), '..', 'CopyFolder')
    
    if not os.path.exists(copy_folder):
        print(f"CopyFolder does not exist at {copy_folder}")
        return
    
    for item in os.listdir(copy_folder):
        s = os.path.join(copy_folder, item)
        d = os.path.join(batch_folder_path, item)

        if os.path.isdir(s):
            # Copy directory
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            # Copy file
            shutil.copy2(s, d)

    print(f"Copied files and folders from CopyFolder to {batch_folder_path}")

