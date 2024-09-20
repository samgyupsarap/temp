import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class LoginView:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Login")

        # Set a fixed window size
        self.root.geometry("500x350")
        self.root.resizable(False, False)  # Prevent resizing

        # Load and set the background image
        self.bg_image = Image.open("./src/bg_py_app.png")  # Path to your image file
        self.bg_image = self.bg_image.resize((500, 350), Image.LANCZOS)  # Resize image using LANCZOS filter
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas and add the background image
        self.canvas = tk.Canvas(self.root, width=500, height=350, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image_tk)

        # Define width for consistency
        self.entry_width = 20  # Adjust this value based on your preference

        # Center the username label
        self.canvas.create_text(250, 80, text="Username", font=("Poppins", 12), fill="black")

        # Username entry with border
        self.username_entry = tk.Entry(
            self.canvas, font=("Poppins", 12), bg='white', width=self.entry_width,
            highlightthickness=2,  # Thickness of the border
            highlightbackground='black',  # Border color when unfocused
            highlightcolor='#0073c2'  # Border color when focused
        )
        self.canvas.create_window(250, 110, window=self.username_entry)

        # Center the password label
        self.canvas.create_text(250, 150, text="Password", font=("Poppins", 12), fill="black")

        # Password entry with border
        self.password_entry = tk.Entry(
            self.canvas, show="*", bg='white', font=("Poppins", 12), width=self.entry_width,
            highlightthickness=2,
            highlightbackground='black',
            highlightcolor='#0073c2'
        )
        self.canvas.create_window(250, 180, window=self.password_entry)

        # Login button with updated styles
        self.login_button = tk.Button(
            self.canvas,
            text="Login",
            command=self.handle_login,
            font=("Poppins", 12),
            bg='#0073c2',  # Custom background color
            fg='white',  # Text color
            activebackground='#448ec2',  # Background color when the button is pressed
            activeforeground='white',  # Text color when the button is pressed
            width=self.entry_width,
            borderwidth=0  # Remove the border
        )
        self.canvas.create_window(250, 240, window=self.login_button)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            self.on_login_success(username, password)
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")