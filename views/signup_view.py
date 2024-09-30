import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
from controllers.signup_controller import SignupController
import os

class SignupView:
    def __init__(self, root, on_signup_success):
        self.root = root
        self.on_signup_success = on_signup_success
        self.controller = SignupController(on_signup_success)

        # Set the window size
        self.width, self.height = 500, 1000
        margin = 30  # Define margin from the screen edges

        # Calculate position on the right side of the screen with margins
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - self.width - margin  # Add margin from the right edge
        y = (screen_height // 2) - (self.height // 2) - margin  # Add margin from the top/bottom
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

        self.root.title("Sign Up")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # Load and set the background image
        try:
            image_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'bg_py_app.png')
            self.bg_image = Image.open(image_path)
            self.bg_image = self.bg_image.resize((self.width, self.height), Image.LANCZOS)
            self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

            icon_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'logo.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            else:
                messagebox.showwarning("Warning", "Icon file not found.")

        except FileNotFoundError:
            messagebox.showerror("Error", "Background image not found.")
            self.root.destroy()  # Close the application if the image is not found

        # Create canvas for the background image
        self.canvas = ctk.CTkCanvas(self.root, width=self.width, height=self.height, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image_tk)

        self.entry_width = 280

        self.canvas.create_text(250, 330, text="Sign Up", font=("Helvetica", 30, "bold"), fill="black")

        # Username entry
        self.username_entry = ctk.CTkEntry(
            self.root, font=("Helvetica", 18), width=self.entry_width, height=60,
            placeholder_text="Enter username", fg_color="white",
            text_color="black",
            placeholder_text_color="#4d4949"
        )
        self.canvas.create_window(250, 400, window=self.username_entry)

        # Password entry
        self.password_entry = ctk.CTkEntry(
            self.root, placeholder_text="Password", show="*", width=self.entry_width, height=60, 
            font=("Helvetica", 18), fg_color="white", text_color="black",
            placeholder_text_color="#4d4949"
        )
        self.canvas.create_window(250, 470, window=self.password_entry)

        # Confirm Password entry
        self.confirm_password_entry = ctk.CTkEntry(
            self.root, placeholder_text="Confirm Password", show="*", width=self.entry_width, height=60, 
            font=("Helvetica", 18), fg_color="white", text_color="black",
            placeholder_text_color="#4d4949"
        )
        self.canvas.create_window(250, 540, window=self.confirm_password_entry)

        # Sign Up button
        self.signup_button = ctk.CTkButton(
            self.root, text="Sign Up", command=self.handle_signup,
            height=70,
            font=("Helvetica", 20, "bold"),
            width=self.entry_width,
            fg_color="#0e8a10",
            hover_color="#448ec2",
            text_color="white",
            background_corner_colors=["white", "white", "white", "white"],
        )
        self.canvas.create_window(250, 615, window=self.signup_button)

        # Back button
        self.back_button = ctk.CTkButton(
            self.root, text="Back", command=self.on_back,
            height=70,
            font=("Helvetica", 20, "bold"),
            width=self.entry_width,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            text_color="white",
            background_corner_colors=["white", "white", "white", "white"]
        )
        self.canvas.create_window(250, 700, window=self.back_button)

        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.on_back()

    def on_back(self):
        self.root.destroy()
        self.on_signup_success()

    def show_custom_message(self, title, message):
        message_window = tk.Toplevel(self.root)
        message_window.title(title)

        # Set the size of the message window
        message_window.geometry("300x120")

        # Center the message window relative to the signup window
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 150  
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 75  
        message_window.geometry(f"300x120+{x}+{y}")

        # Add a label for the message
        label = tk.Label(message_window, text=message, padx=10, pady=10)
        label.pack()

        # Add an OK button to close the message window
        ok_button = tk.Button(message_window, text="OK", command=message_window.destroy)
        ok_button.pack(pady=(0, 10))

    def handle_signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Check if the passwords match
        if password != confirm_password:
            self.show_custom_message("Signup Failed", "Passwords do not match!")
            return

        # Replace with your actual signup logic
        if self.controller.signup_user(username, password):  # Assuming this returns True on success
            # Create an indicator file after successful signup
            with open("success.txt", "w") as f:  # Create an indicator file
                f.write("User signed up successfully.")

            self.on_signup_success()  # Notify success to the LoginView
            self.root.destroy()  # Close the signup window
        else:
            self.show_custom_message("Signup Failed", "Signup failed. Please try again.")
