import customtkinter as ctk
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
        self.canvas = ctk.CTkCanvas(self.root, width=500, height=350, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image_tk)

        # Consistent width for entry fields and buttons
        self.entry_width = 200  # Adjust the pixel width for entries and buttons

        # Create a label for CaseID (centered)
        self.canvas.create_text(250, 70, text="Enter CaseID", font=("Helvetica", 12, "bold"), fill="black")

        # CaseID entry with white background
        self.caseid_entry = ctk.CTkEntry(
            self.canvas, font=("Helvetica", 14), width=self.entry_width, height=40,
            placeholder_text="Enter CaseID", fg_color="white", text_color="black", 
            placeholder_text_color="#4d4949"
        )
        self.canvas.create_window(250, 110, window=self.caseid_entry)

        # Create a label for Number of Batches (centered)
        self.canvas.create_text(250, 150, text="Number of Batches", font=("Helvetica", 12, "bold"), fill="black")

        # Number of Batches entry with white background
        self.batches_entry = ctk.CTkEntry(
            self.canvas, font=("Helvetica", 14), width=self.entry_width, height=40,
            placeholder_text="Enter number of batches", fg_color="white", text_color="black", 
            placeholder_text_color="#4d4949"
        )
        self.canvas.create_window(250, 190, window=self.batches_entry)

        # Submit button with custom style
        self.submit_button = ctk.CTkButton(
            self.canvas, text="Submit", font=("Helvetica", 14), height=50, width=self.entry_width,
            fg_color="#0073c2", hover_color="#448ec2",  text_color="white", command=self.submit
        )
        self.canvas.create_window(250, 245, window=self.submit_button)

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


if __name__ == "__main__":
    root = ctk.CTk()
    app = MainView(root)
    root.mainloop()
    app.center_window(500, 350) 