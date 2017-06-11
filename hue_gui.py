from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

import hue


class PowerButtons(BoxLayout):
    def __init__(self, **kwargs):
        super(PowerButtons, self).__init__(orientation='horizontal', **kwargs)
        self.on_button = Button(text='On')
        self.on_button.bind(on_press=self.power_on)
        self.add_widget(self.on_button)
        self.off_button = Button(text='Off')
        self.off_button.bind(on_press=self.power_off)
        self.add_widget(self.off_button)

    def power_on(self, instance):
        hue.power_on()

    def power_off(self, instance):
        hue.power_off()


class MyApp(App):
    title = "Hue Control"

    def build(self):
        return PowerButtons()


if __name__ == '__main__':
    MyApp().run()
