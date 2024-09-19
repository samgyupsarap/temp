from models.token_model import TokenStorage  # Import TokenStorage to save the token
from models.api_model import login
import tkinter as tk
from views.main_view import MainView
from tkinter import messagebox

class LoginController:
    def __init__(self, root):
        self.root = root

    def handle_login(self, username, password):
        try:
            token = login(username, password)
            print(f"Login successful. Token: {token}")  # Print the token to the terminal

            # Save the token to TokenStorage
            TokenStorage.set_token(token)

            messagebox.showinfo("Login Success", "Logged in successfully.")
            self.root.destroy()  # Close the login window

            # Initialize MainView
            root = tk.Tk()
            MainView(root)
            root.mainloop()

        except RuntimeError as e:
            messagebox.showerror("Login Error", str(e))
