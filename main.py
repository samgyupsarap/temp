import tkinter as tk
from tkinter import messagebox  # Import messagebox for showing dialog boxes
from controllers.login_controller import LoginController
from views.login_view import LoginView
import threading
import customtkinter as ctk
ctk.set_appearance_mode("light")

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x300")
        self.login_controller = LoginController(self)
        self.login_view = LoginView(self, self.on_login_success)
        self.thread = None  # To track any background thread

    def on_login_success(self, username, password):
        # Handle login success logic here
        self.login_controller.handle_login(username, password)

    def on_closing(self):
        """Handle the close event of the main window."""
        if self.thread and self.thread.is_alive():
            if messagebox.askokcancel("Quit", "Batch processing is still running. Are you sure you want to quit?"):
                self.destroy()  # Destroy the main window
        else:
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.destroy()  # Destroy the main window

def main():
    app = Application()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)  # Bind the close event
    app.mainloop()  # Start the Tkinter event loop

if __name__ == "__main__": 
    main()
