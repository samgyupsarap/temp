import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from controllers.data_controller import handle_submit  # Import the new function
import os

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Finding GeoID")
        self.root.geometry("500x1000")
        self.root.resizable(False, False)

        # Load and set the background image
        try:
            image_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'bg_py_app.png')
            self.bg_image = Image.open(image_path)
            self.bg_image = self.bg_image.resize((500, 1000), Image.LANCZOS)
            self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)
        except FileNotFoundError:
            messagebox.showerror("Error", "Background image not found.")
            self.root.destroy()  # Close the application if the image is not found

        # Create a canvas to hold the background image and widgets
        self.canvas = ctk.CTkCanvas(self.root, width=500, height=1000, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image_tk)

        # Consistent width for entry fields and buttons
        self.entry_width = 300  # Adjust the pixel width for entries and buttons

        # Create a label for CaseID (centered)
        self.canvas.create_text(250, 330, text="GeoID", font=("Helvetica", 16, "bold"), fill="black")

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
            fg_color="#0073c2", hover_color="#005ea6", text_color="white", command=self.confirm_submit
        )
        self.canvas.create_window(250, 600, window=self.submit_button)

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def confirm_submit(self):
        caseid_pattern = self.caseid_entry.get().strip()
        records_per_batch = self.records_entry.get().strip()

        # Validate inputs
        if not caseid_pattern:
            messagebox.showwarning("Input Error", "Please enter a GeoID pattern.")
            return

        if records_per_batch:
            try:
                records_per_batch = int(records_per_batch)
                if records_per_batch <= 0:
                    raise ValueError("Number of records must be positive.")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid number for records per batch.")
                return
        else:
            records_per_batch = 1000  # Default value

        # Show confirmation dialog
        confirm = messagebox.askyesno("Confirm Submission", f"Are you sure you want to submit?\nGeoID: {caseid_pattern}\nRecords per Batch: {records_per_batch}")
        if confirm:
            # Call the handle_submit function from data_controller
            handle_submit(caseid_pattern, records_per_batch)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()  # Safely destroy the app

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainView(root)
    root.mainloop()
