import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox
from controllers.signup_controller import SignupController  # Import the controller
import os
ctk.set_appearance_mode("light")

class SignupView:
    def __init__(self, root, on_signup_success):
        self.root = root
        self.on_signup_success = on_signup_success
        self.controller = SignupController(on_signup_success)  # Pass the callback to controller
        self.root.title("Sign Up")

        self.root.geometry("500x1000")
        self.root.resizable(False, False)

        # Load and set the background image
        try:
            image_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'bg_py_app.png')
            self.bg_image = Image.open(image_path)
            self.bg_image = self.bg_image.resize((500, 1000), Image.LANCZOS)  # Resize image using LANCZOS filter
            self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)
        except FileNotFoundError:
            messagebox.showerror("Error", "Background image not found.")
            self.root.destroy()  # Close the application if the image is not found

        # Create canvas for the background image
        self.canvas = ctk.CTkCanvas(self.root, width=500, height=1000, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image_tk)

        self.entry_width = 280  # Adjust the pixel width for entries

        self.canvas.create_text(250, 320, text="Sign Up", font=("Helvetica", 30, "bold"), fill="black")

        # Username entry
        self.username_entry = ctk.CTkEntry(
            self.canvas, font=("Helvetica", 18), width=self.entry_width, height=60,
            placeholder_text="Enter username", fg_color="white",  # White background
            text_color="black",
            placeholder_text_color="#4d4949"
        )
        self.canvas.create_window(250, 400, window=self.username_entry)

        # Password entry
        self.password_entry = ctk.CTkEntry(
            self.canvas, placeholder_text="Password", show="*", width=self.entry_width, height=60, 
            font=("Helvetica", 18), fg_color="white", text_color="black",
            placeholder_text_color="#4d4949"
        )
        self.canvas.create_window(250, 470, window=self.password_entry)

        # Sign Up button
        self.signup_button = ctk.CTkButton(
            self.canvas, text="Sign Up", command=self.handle_signup,
            height=70,
            font=("Helvetica", 20, "bold"),
            width=self.entry_width,
            fg_color="#0e8a10",  # Button background color
            hover_color="#448ec2",  # Hover background color
            text_color="white"  # Text color
        )
        self.canvas.create_window(250, 540, window=self.signup_button)

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def handle_signup(self):
        username = self.username_entry.get().strip()  # Get the username from the entry
        password = self.password_entry.get().strip()  # Get the password from the entry

        # Validate inputs
        if not username or not password:
            messagebox.showwarning("Input Error", "Both username and password are required.")
            return
        if len(password) < 6:  # Example condition: password must be at least 6 characters
            messagebox.showwarning("Input Error", "Password must be at least 6 characters long.")
            return

        # Call the signup function in the controller
        result = self.controller.signup_user(username, password)

        if result is True:
            messagebox.showinfo("Signup Success", "You have successfully signed up!")
            self.root.after(100, self.close_signup)  # Close the signup window after a short delay
        else:
            messagebox.showwarning("Signup Failed", result)  # Show error message

    def close_signup(self):
        self.root.destroy()  # Close the signup window
        self.on_signup_success()  # Call the on_signup_success method of the LoginView

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            try:
                self.root.destroy()  # Safely destroy the app
            except Exception as e:
                print(f"Error while closing the application: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = SignupView(root, lambda: print("Signup successful!"))
    root.mainloop()
