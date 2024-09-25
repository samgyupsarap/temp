
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox
from controllers.signup_controller import SignupController  # Import the controller

class SignupView:
    def __init__(self, root, on_signup_success):
        self.root = root
        self.on_signup_success = on_signup_success
        self.controller = SignupController(on_signup_success)  # Pass the callback to controller
        self.root.title("Sign Up")

        self.root.geometry("500x1000")
        self.root.resizable(False, False)

        # Load and set the background image
        self.bg_image = Image.open("./src/bg_py_app.png")  # Path to your image file
        self.bg_image = self.bg_image.resize((500, 1000), Image.LANCZOS)  # Resize image using LANCZOS filter
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        # Create canvas for the background image
        self.canvas = ctk.CTkCanvas(self.root, width=500, height=1000, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image_tk)

        self.entry_width = 280  # Adjust the pixel width for entries

        self.canvas.create_text(250, 350, text="Sign Up", font=("Helvetica", 30, "bold"), fill="black")
        # Username entry
        self.username_entry = ctk.CTkEntry(
            self.root, font=("Helvetica", 18), width=self.entry_width, height=60,
            placeholder_text="Enter username", fg_color="white",  # White background
            text_color="black",
            placeholder_text_color="#4d4949"
        )
        self.canvas.create_window(250, 400, window=self.username_entry)

        # Password entry
        self.password_entry = ctk.CTkEntry(
            self.root, placeholder_text="Password", show="*", width=self.entry_width, height=60, font=("Helvetica", 18), fg_color="white",  text_color="black",
            placeholder_text_color="#4d4949"
        )
        self.canvas.create_window(250, 470, window=self.password_entry)

        # Sign Up button
        self.signup_button = ctk.CTkButton(
            self.root, text="Sign Up", command=self.handle_signup,
            height=70,
            font=("Helvetica", 20, "bold"),
            width=self.entry_width,
            fg_color="#0e8a10",  # Button background color
            hover_color="#448ec2",  # Hover background color
            text_color="white"  # Text color
        )
        self.canvas.create_window(250, 540, window=self.signup_button)

    def handle_signup(self):
        username = self.username_entry.get()  # Get the username from the entry
        password = self.password_entry.get()  # Get the password from the entry
        
        result = self.controller.signup_user(username, password)  # Pass values to controller

        if result is True:
            messagebox.showinfo("Signup Success", "You have successfully signed up!")
            self.root.destroy()  # Close the signup window only
            # Call the on_signup_success method of the LoginView
            self.on_signup_success()  
        else:
            messagebox.showwarning("Signup Failed", result)  # Show error message


