import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox
from controllers.login_controller import LoginController
from views.signup_view import SignupView
import os

class LoginView:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.controller = LoginController(root)
        
        # Check if user is already signed up
        self.user_signed_up = self.check_user_signup_status()
        
        self.setup_ui()  # Set up the UI components

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        width, height = 500, 1000
        margin = 30  # Define margin from the screen edges

        self.root.geometry(f"{width}x{height}")

        # Calculate position on the right side of the screen with margins
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - width - margin  # Add margin from the right edge
        y = (screen_height // 2) - (height // 2) - margin  # Add margin from the top/bottom
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.resizable(False, False)

    def check_user_signup_status(self):
        signup_file = './signup.txt'  # Update this to your actual signup file path
        return os.path.exists(signup_file)

    def setup_ui(self):
        self.root.title("Login")
        self.root.geometry("500x1000")
        self.root.resizable(False, False)

        # Load and set the background image
        try:
            image_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'bg_py_app.png')
            self.bg_image = Image.open(image_path)
            self.bg_image = self.bg_image.resize((500, 1000), Image.LANCZOS)
            self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

            icon_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'logo.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)

        except FileNotFoundError:
            messagebox.showerror("Error", "Background image not found.")
            self.root.destroy()  # Close the application if the image is not found

        self.canvas = ctk.CTkCanvas(self.root, width=500, height=1000, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image_tk)

        self.entry_width = 280  # Adjust the pixel width for entries
        self.canvas.create_text(250, 320, text="Login", font=("Helvetica", 30, "bold"), fill="black")

        self.username_entry = ctk.CTkEntry(
            self.canvas, font=("Helvetica", 18), width=self.entry_width, height=60,
            placeholder_text="Username", fg_color="white", 
            text_color="black", placeholder_text_color="#4d4949"
        )
        self.canvas.create_window(250, 400, window=self.username_entry)

        self.password_entry = ctk.CTkEntry(
            self.canvas, placeholder_text="Password", show="*", width=self.entry_width, height=60,
            font=("Helvetica", 18), fg_color="white", text_color="black",
            placeholder_text_color="#4d4949"
        )
        self.canvas.create_window(250, 470, window=self.password_entry)

        self.login_button = ctk.CTkButton(
            self.canvas, text="Login", command=self.handle_login,
            height=70, font=("Helvetica", 20, "bold"),
            width=self.entry_width, fg_color="#0073c2", 
            hover_color="#448ec2", text_color="white"
        )
        self.canvas.create_window(250, 545, window=self.login_button)

        # Conditionally show the signup button
        self.signup_button = None  # Initialize signup_button as None
        self.create_signup_button()  # Method to create the signup button

    def create_signup_button(self):
        """Create the signup button if the signup.txt file is not present."""
        if not self.user_signed_up:  # Check if the signup file does not exist
            self.signup_button = ctk.CTkButton(
                self.canvas, text="Sign Up", command=self.open_signup,
                height=70, font=("Helvetica", 20, "bold"),
                width=self.entry_width, fg_color="#0e8a10",
                hover_color="#448ec2", text_color="white"
            )
            self.canvas.create_window(250, 630, window=self.signup_button)

    def handle_login(self):
        username = self.username_entry.get()  # Get the username from the entry
        password = self.password_entry.get()  # Get the password from the entry

        # Call the login controller to handle the login process
        if self.controller.handle_login(username, password):
            # If login is successful, clear entries
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.on_login_success(username, password)  # Call success callback

    def open_signup(self):
        self.root.withdraw()  # Hide the login window
        signup_window = ctk.CTkToplevel(self.root)  # Create a new top-level window
        SignupView(signup_window, self.on_signup_success)  # Pass the signup success callback

    def on_signup_success(self):
        # When signup is successful, update the state
        self.user_signed_up = True  # Update the state
        self.hide_signup_button()  # Call the method to hide the signup button

        # Delay showing the login window by 1000 milliseconds (1 second)
        self.root.after(1000, self.refresh_login_window)  # Call refresh_login_window after delay

    def hide_signup_button(self):
        """Hide the signup button if it exists."""
        if self.signup_button:
            self.signup_button.pack_forget()  # This line hides the signup button
            self.signup_button = None  # Clear the reference to the button

    def refresh_login_window(self):
        # Refresh the user signup status
        self.user_signed_up = self.check_user_signup_status()

        # Clear the entries and refresh the UI
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

        # Remove the signup button if the user is signed up
        if self.user_signed_up and self.signup_button:
            self.signup_button.pack_forget()  # Hide the signup button if user is signed up
            self.signup_button = None  # Clear the reference to the button

        # Show the login window again
        self.root.deiconify()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()  # Safely destroy the app
