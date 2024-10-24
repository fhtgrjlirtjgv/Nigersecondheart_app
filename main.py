from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager
import requests
from settings import *


class WeatherCard(MDCard):
    def __init__(self, weather, *args, **kwargs):
        super().__init__(*args, **kwargs)
        temp = weather["main"]["temp"]
        self.ids.temp.text = f"{round(temp)}°C"
        desc = weather["weather"][0]["description"]
        self.ids.desc.text = desc.capitalize()
        icon = weather["weather"][0]["icon"]
        self.ids.icon.source = f'https://openweathermap.org/img/wn/{icon}@2x.png'
        date_time = weather["dt_txt"]
        self.ids.date.text = f"{date_time[5:16]}"


class ForeCastScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'

    def get_forecast(self, city):
        params = {
            "q": city,
            "appid": API_KEY,
        }
        data = requests.get(FORECAST_URL, params)
        response = data.json()
        return response['list'] 

    def show_forecast(self, forecast):
        #додаємо картки з прогнозом погоди кожні 6 годин
        for i in range(0, len(forecast), 2):
            data = forecast[i]
            card = WeatherCard(data)
            self.ids.weather_list.add_widget(card)


class WScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.city = 'Львів'

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
        self.city = self.ids.city.text
        weather = self.get_weather(self.city)

        temp = weather["main"]["temp"]
        self.ids.temp.text = f"{round(temp)}°C"
        
        feels_like = weather["main"]["feels_like"]
        self.ids.feels_like.text = f"Відчувається як {round(feels_like)}°C"

        desc = weather["weather"][0]["description"]
        self.ids.desc.text = desc.capitalize()

        humidity = weather["main"]["humidity"]
        self.ids.humidity.text = f"Вологість: {humidity}%"

        wind = weather["wind"]["speed"]
        self.ids.wind.text = f"Вітер: {wind} м/c"

        forecast_data = self.forecast.get_forecast(self.city)
        self.forecast.show_forecast(forecast_data)

    def show_forecast(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'forecast'

class LCW(MDApp):
    def build(self):
        Builder.load_file('Been.kv')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        sm = MDScreenManager()
        self.weather_screen = WScreen(name='home')
        self.forecast_screen = ForeCastScreen(name='forecast')
        self.weather_screen.forecast = self.forecast_screen
        sm.add_widget(self.weather_screen)
        sm.add_widget(self.forecast_screen)
        return sm   
    

LCW ().run()