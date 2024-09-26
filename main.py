from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton
from kivy.lang import Builder
import requests
from settings import *


class WScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def get_weather(self, city):
        params = {
            "q": city,
            "appid": API_KEY,
        }
        data = requests.get(CURRENT_WEATHER_URL, params)
        respons = data.json()
        print(respons)
        return respons

    def search(self):
        city = self.ids.city.text
        weather = self.get_weather(city)

        temp = weather["main"]["temp"]
        self.ids.temp.text = f"{round(temp)}°C"
        



class LCW(MDApp):
    def build(self):
        Builder.load_file('Been.kv')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"

        return WScreen()
    

LCW ().run()