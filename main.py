from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton
from kivy.lang import Builder

class WScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LCWApp(MDApp):
    def build(self):
        Builder.load_file('Been.kv')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"

        return WScreen() (
            MDScreen(
                MDRectangleFlatButton(
                    text="Hello, World",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
            )
        )


LCWApp().run()