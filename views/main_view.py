import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image, ImageTk
from controllers.data_controller import process_batches

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Finding CaseID")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        # Load and set the background image
        self.bg_image = Image.open("./src/bg_py_app.png")  # Path to your background image
        self.bg_image = self.bg_image.resize((500, 350), Image.LANCZOS)  # Resize image to fit the window
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas to hold the background image and widgets
        self.canvas = tk.Canvas(self.root, width=500, height=350, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image_tk)

        # Consistent width for entry fields and buttons
        self.entry_width = 20

        # Create a label for CaseID (centered)
        self.canvas.create_text(250, 80, text="Enter CaseID", font=("Poppins", 12), fill="black")

        # Create an entry widget for CaseID input with a border
        self.caseid_entry = tk.Entry(
            self.canvas, font=("Poppins", 12), bg='white', width=self.entry_width,
            highlightthickness=2,  # Thickness of the border
            highlightbackground='black',  # Border color when unfocused
            highlightcolor='#0073c2'
        )
        self.canvas.create_window(250, 110, window=self.caseid_entry)

        # Create a label for Number of Batches (centered)
        self.canvas.create_text(250, 150, text="Number of Batches", font=("Poppins", 12), fill="black")

        # Create an entry widget for Number of Batches input with a border
        self.batches_entry = tk.Entry(
            self.canvas, font=("Poppins", 12), bg='white', width=self.entry_width,
            highlightthickness=2,  # Thickness of the border
            highlightbackground='black',  # Border color when unfocused
            highlightcolor='#0073c2'  # Border color when focused
        )
        self.canvas.create_window(250, 180, window=self.batches_entry)

        self.submit_button = tk.Button(
            self.canvas,
            text="Submit",
            command=self.submit,
            font=("Poppins", 12),
            bg='#0073c2',  # Custom background color (e.g., green)
            fg='white',  # Text color
            activebackground='#448ec2',  # Background color when the button is pressed
            activeforeground='white',  # Text color when the button is pressed
            width=self.entry_width,  # Button width to match the input fields
            borderwidth=0  # Remove the border
        )
        self.canvas.create_window(250, 240, window=self.submit_button)

    def submit(self):
        user_input = self.caseid_entry.get()
        num_batches_input = self.batches_entry.get()

        if user_input.isdigit() and num_batches_input.isdigit():
            folder_name = f"{user_input}"
            num_batches = int(num_batches_input)

            # Ask the user to choose a directory
            folder_path = filedialog.askdirectory(title="Select Directory")

            if folder_path:
                # Create the CaseID folder in the selected directory
                full_path = os.path.join(folder_path, folder_name)

                try:
                    # Process batches
                    process_batches(full_path, user_input, num_batches)
                    messagebox.showinfo("Success", f"Folder '{folder_name}' and all batch folders created with data.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showwarning("No Directory Selected", "Please select a directory.")
        else:
            messagebox.showwarning("Invalid input", "Please enter valid numbers for CaseID and Number of Batches.")
