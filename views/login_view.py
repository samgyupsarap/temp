# views/login_view.py
import tkinter as tk
from tkinter import messagebox
from controllers.login_controller import LoginController

class LoginView:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Login")
        self.root.geometry("300x300")

        tk.Label(self.root, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.handle_login).pack(pady=20)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            self.on_login_success(username, password)
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
