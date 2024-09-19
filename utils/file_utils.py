import os

def create_folder_if_not_exists(parent_folder, folder_name):

    batch_folder_path = os.path.join(parent_folder, folder_name)
    if os.path.exists(batch_folder_path):

        batch_folder_path = os.path.join(parent_folder, f"{folder_name} (new)")
    os.makedirs(batch_folder_path, exist_ok=True)
    return batch_folder_path


def save_data_to_file(folder_path, batch_no, api_data):
    """Save the API data to a text file."""
    txt_file_path = os.path.join(folder_path, f"Batch_{batch_no}.txt")

    try:
        with open(txt_file_path, "w") as file:
            for item in api_data:
                # Ensure that item is a dictionary and contains 'caseid'
                if isinstance(item, dict) and 'caseid' in item:
                    file.write(f"{item['caseid']}\n")
                else:
                    # Log or handle unexpected data
                    print(f"Unexpected item format: {item}")

        print(f"Data successfully saved in {txt_file_path}")
    except Exception as e:
        print(f"Error saving data to file: {e}")

    # Create a text file for the complete path
    path_file_path = os.path.join(folder_path, "batch_path.txt")
    with open(path_file_path, "w") as path_file:
        path_file.write(f"{folder_path}")


