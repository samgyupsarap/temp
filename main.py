# main.py
import tkinter as tk
from controllers.login_controller import LoginController
from views.login_view import LoginView


def main():
    root = tk.Tk()
    root.geometry("300x300")

    def on_login_success(username, password):
        login_controller.handle_login(username, password)

    login_controller = LoginController(root)
    login_view = LoginView(root, on_login_success)

    root.mainloop()


if __name__ == "__main__":
    main()
