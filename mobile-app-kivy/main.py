from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from files.hoverable import HoverBehavior
from datetime import datetime
from pathlib import Path
from random import choice
import json, glob


# load GUI
Builder.load_file('files/gui.kv')

class LoginScreen(Screen):
    """App's login page"""
    def sign_up(self):
        self.manager.transition.direction = "left"
        self.manager.current = "sign_up_screen"
    
    def login(self, user, passw):
        with open("files/users.json", "r") as file:
            users = json.load(file)
        if user in users:
            if users[user]['password'] == passw:
                self.manager.transition.direction = "left"
                self.manager.current = "login_screen_success"
            else:
                self.ids.info_label.text = "Wrong password"
        else:
            self.ids.info_label.text = "Wrong username"
            # delete next two lines after testing
            self.manager.transition.direction = "left"
            self.manager.current = "login_screen_success"


class LoginScreenSuccess(Screen):
    """MAIN PAGE after user login was successful"""
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
    
    def get_quote(self, mood):
        available_moods = [Path(filename).stem for filename in glob.glob("quotes/*.txt")]
        if mood.lower() in available_moods:
            with open(f"quotes/{mood}.txt", "r", encoding="utf-8") as file:
                quotes = file.readlines()
            self.ids.quote.text = choice(quotes)
        elif not mood:
            self.ids.quote.text = "Empty feelings..."
        else:
            self.ids.quote.text = f"No quotes found for mood '{mood}'"


class SignUpScreen(Screen):
    """App's signup page"""
    def add_user(self, user, passw):
        # read current json
        if user and passw:
            with open("files/users.json", "r") as file:
                users = json.load(file)
            # insert data
            users[user] = {
                "username": user,
                "password": passw,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            # update json
            with open("files/users.json", "w") as file:
                json.dump(users, file)
            self.manager.transition.direction = "left"
            self.manager.current = "sign_up_screen_success"
        else:
            self.ids.info_label.text = "Invalid input"
    
    def to_main(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


class SignUpScreenSuccess(Screen):
    """Informs user the signup was successful"""
    def to_main(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class RootWidget(ScreenManager):
    """docstring"""
    pass


class MainApp(App):
    """App's func"""
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MainApp().run()
