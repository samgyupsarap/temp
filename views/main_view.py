# views/main_view.py
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from controllers.data_controller import process_batches

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Finding CaseID")
        self.root.geometry("500x200")

        # Create a label for CaseID
        self.label = tk.Label(root, text="Enter CaseID:")
        self.label.pack(pady=10)

        # Create an entry widget for CaseID input
        self.entry = tk.Entry(root)
        self.entry.pack(pady=5)

        # Create a submit button
        self.submit_button = tk.Button(root, text="Submit", command=self.submit)
        self.submit_button.pack(pady=10)

    def submit(self):
        user_input = self.entry.get()

        if user_input.isdigit():
            folder_name = f"{user_input}"

            # Ask the user to choose a directory
            folder_path = filedialog.askdirectory(title="Select Directory")

            if folder_path:
                # Create the CaseID folder in the selected directory
                full_path = os.path.join(folder_path, folder_name)

                try:
                    # Process batches
                    process_batches(full_path, user_input)
                    messagebox.showinfo("Success", f"Folder '{folder_name}' and all batch folders created with data.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showwarning("No Directory Selected", "Please select a directory.")
        else:
            messagebox.showwarning("Invalid input", "Please enter a valid number.")
