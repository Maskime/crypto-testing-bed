from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from mongoengine import connect

import configuration as cfg
from documents.binance import TwentyFourHrTickerEvent


class Exploration(BoxLayout):
    symbols_buttons = ObjectProperty(None)
    symbols_graph = ObjectProperty(None)

    delay_milliseconds = 300

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        connect(**cfg.mongo_params)
        if self.symbols_buttons is None:
            print('Starting scheduler')
            Clock.schedule_interval(self.load_buttons, 0.05)

    def load_buttons(self, dt):
        print('Trying to load buttons')
        if self.symbols_buttons is None:
            return True
        print('Loading buttons')
        symbols = TwentyFourHrTickerEvent.get_symbols()
        print('Loading {} buttons'.format(len(symbols)))
        for symbol in symbols:
            self.symbols_buttons.add_widget(ToggleButton(text=symbol, size_hint_y=None, height=40))
        print('Buttons loaded')
        return False
