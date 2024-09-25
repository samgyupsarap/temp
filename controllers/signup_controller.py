from models.api_model import signup

class SignupController:
    def __init__(self, on_signup_success):
        self.on_signup_success = on_signup_success

    def signup_user(self, username, password):
        if username and password:
            try:
                signup(username, password)
                return True
            except RuntimeError as e:
                return str(e)  
        return "Please enter both username and password."
