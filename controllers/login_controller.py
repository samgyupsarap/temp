from models.api_model import login
from views.main_view import MainView
from tkinter import Tk, messagebox

class LoginController:
    def __init__(self, root):
        self.root = root

    def handle_login(self, username, password):
        try:
            token = login(username, password)
            messagebox.showinfo("Login Success", "Logged in successfully.")
            self.root.destroy()  # Close the login window

            # Initialize MainView
            root = Tk()
            MainView(root)
            root.mainloop()
        except RuntimeError as e:
            messagebox.showerror("Login Error", str(e))
