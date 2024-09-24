import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from PIL import Image, ImageTk
from controllers.data_controller import process_batches

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Finding CaseID")
        self.root.geometry("500x1000")
        self.root.resizable(False, False)

        # Load and set the background image
        self.bg_image = Image.open("./src/bg_py_app.png")  # Path to your background image
        self.bg_image = self.bg_image.resize((500, 1000), Image.LANCZOS)  # Resize image to fit the window
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas to hold the background image and widgets
        self.canvas = ctk.CTkCanvas(self.root, width=500, height=1000, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image_tk)

        # Consistent width for entry fields and buttons
        self.entry_width = 300  # Adjust the pixel width for entries and buttons

        # Create a label for CaseID (centered)
        self.canvas.create_text(250, 330, text="CaseID", font=("Helvetica", 16, "bold"), fill="black")

        # CaseID entry with white background
        self.caseid_entry = ctk.CTkEntry(
            self.canvas, font=("Helvetica", 18), width=self.entry_width, height=60,
            fg_color="white", text_color="black"
        )
        self.canvas.create_window(250, 380, window=self.caseid_entry)

        # Create a label for Number of Records (centered)
        self.canvas.create_text(250, 450, text="Number of Records per Batch", font=("Helvetica", 16, "bold"), fill="black")

        # Number of Records entry with white background
        self.records_entry = ctk.CTkEntry(
            self.canvas, font=("Helvetica", 18), width=self.entry_width, height=60,
            placeholder_text="Default: 1000", fg_color="white", text_color="black",
            placeholder_text_color="#4d4949"
        )
        self.canvas.create_window(250, 500, window=self.records_entry)

        # Submit button with custom style
        self.submit_button = ctk.CTkButton(
            self.canvas, text="Submit", font=("Helvetica", 20, "bold"), height=70, width=self.entry_width,
            fg_color="#0073c2", hover_color="#448ec2", text_color="white", command=self.submit
        )
        self.canvas.create_window(250, 580, window=self.submit_button)

    def submit(self):
        user_input = self.caseid_entry.get()
        records_input = self.records_entry.get()

        # Validate CaseID input
        if not user_input.isdigit():
            messagebox.showwarning("Invalid input", "Please enter a valid CaseID.")
            return

        folder_name = f"{user_input}"

        # Validate and parse the number of records per batch input
        if records_input.isdigit():
            records_per_batch = int(records_input)
        elif not records_input:  # If no input, default to 1000
            records_per_batch = 1000
        else:
            messagebox.showwarning("Invalid input", "Please enter a valid number for records per batch.")
            return

        # Ask the user to choose a directory
        folder_path = filedialog.askdirectory(title="Select Directory")

        if not folder_path:
            messagebox.showwarning("No Directory Selected", "Please select a directory.")
            return

        # Calculate the total number of records (for example, 5 million as a fixed value)
        total_records = 5000000  # You can adjust this value as needed

        # Calculate the total number of batches
        num_batches = (total_records + records_per_batch - 1) // records_per_batch

        # Show a confirmation message with the total number of batches
        confirm_message = f"This operation will generate {num_batches} batches, each with up to {records_per_batch} records.\n\nDo you want to proceed?"
        confirm = messagebox.askyesno("Confirm Batch Generation", confirm_message)

        if not confirm:
            return  # Stop processing if the user selects 'No'

        # Create the CaseID folder in the selected directory
        full_path = os.path.join(folder_path, folder_name)

        try:
            # Process batches, passing the validated records_per_batch
            process_batches(full_path, user_input, records_per_batch)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainView(root)
    root.mainloop()
