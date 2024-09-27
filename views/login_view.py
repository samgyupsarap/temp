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
        self.controller = LoginController(root)  # Initialize the login controller
        self.setup_ui()  # Set up the UI components

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

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
            placeholder_text="Enter username", fg_color="white", 
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
        else:
            return

    def open_signup(self):
        self.root.withdraw()  # Hide the login window
        signup_window = ctk.CTkToplevel(self.root)  # Create a new top-level window
        SignupView(signup_window, self.on_signup_success)  # Pass the login success callback

    def on_signup_success(self):
        # When signup is successful, show the login window again
        self.root.deiconify()  # Show the login window again

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()  # Safely destroy the app

if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginView(root, lambda u, p: print(f"Logged in with {u} and {p}"))
    root.mainloop()
