from typing import Dict

from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from mongoengine import connect
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

import configuration as cfg
from documents.binance import TwentyFourHrTickerEvent


class Exploration(BoxLayout):
    symbols_buttons = ObjectProperty(None)
    symbols_graph = ObjectProperty(None)
    check_delay: float = 0.05

    displayed_symbol: Dict[str, bool] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        connect(**cfg.mongo_params)
        if self.symbols_buttons is None:
            Clock.schedule_interval(self.load_buttons, self.check_delay)

    def load_buttons(self, dt):
        if self.symbols_buttons is None:
            return True
        symbols = TwentyFourHrTickerEvent.get_symbols()
        for symbol in symbols:
            symbol_button = ToggleButton(text=symbol, size_hint_y=None, height=40)
            symbol_button.bind(state=self.update_graph)
            self.symbols_buttons.add_widget(symbol_button)
        return False

    def load_graphs(self, dt):
        print('loading graph')
        if self.symbols_graph is None:
            Clock.schedule_interval(self.load_graphs, self.check_delay)
        plt.plot([1, 2, 3])
        plt.ylabel('Prout')
        self.symbols_graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def update_graph(self, instance: ToggleButton, state):
        symbol = instance.text
        print(symbol, state)
        if symbol in self.displayed_symbol:
            self.displayed_symbol[symbol] = not self.displayed_symbol[symbol]
        else:
            self.displayed_symbol[symbol] = True

        if self.symbols_graph is None:
            Clock.schedule_interval(self.load_graphs, self.check_delay)
        else:
            self.load_graphs(None)
