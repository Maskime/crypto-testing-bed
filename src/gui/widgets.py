from typing import Dict

import matplotlib.pyplot as plt
from kivy.clock import Clock
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.properties import ObjectProperty
from kivy.uix.actionbar import ActionToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from matplotlib.lines import Line2D
from mongoengine import connect
import numpy as np

import configuration as cfg
from documents.binance import TwentyFourHrTickerEvent


class Exploration(BoxLayout):
    symbols_buttons = ObjectProperty(None)
    symbols_graph = ObjectProperty(None)
    market_filter = ObjectProperty(None)

    check_delay: float = 0.05

    displayed_symbol: Dict[str, bool] = {}
    graph_added = False

    displayed_market: Dict[str, bool] = {}
    symbols_buttons_list: Dict[str, ToggleButton] = {}
    symbols_lines: Dict[str, Line2D] = {}

    fig = None
    ax = None
    graph_canvas = None

    current_min = None
    current_max = None
    margin = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        connect(**cfg.mongo_params)
        if self.symbols_buttons is None:
            Clock.schedule_interval(self.load_buttons, self.check_delay)

    def load_buttons(self, dt):
        if self.symbols_buttons is None:
            return True
        for market in cfg.markets:
            button = ActionToggleButton(text=market, state='normal')
            button.bind(state=self.update_marketfilter)
            self.market_filter.add_widget(button)
            self.displayed_market[market] = False
        return False

    def add_symbolbutton(self, symbol):
        symbol_button = ToggleButton(text=symbol, size_hint_y=None, height=40)
        symbol_button.bind(state=self.symbol_button_callback)
        self.symbols_buttons_list[symbol] = symbol_button
        self.symbols_buttons.add_widget(symbol_button)

    def filter_market(self):
        to_show = [market for market in self.displayed_market if self.displayed_market[market]]
        print('Markets to show', to_show)
        for symbol in self.symbols_buttons_list.keys():
            self.symbols_buttons.remove_widget(self.symbols_buttons_list[symbol])
        self.symbols_buttons_list = {}
        if len(to_show) > 0:
            for market in to_show:
                symbols = TwentyFourHrTickerEvent.get_symbols(market)
                for symbol in symbols:
                    self.add_symbolbutton(symbol)

    def update_marketfilter(self, instance, state):
        print(instance.text, state)
        self.displayed_market[instance.text] = not self.displayed_market[instance.text]

        self.filter_market()

    def init_graph(self):
        if self.graph_added:
            return
        self.fig, self.ax = plt.subplots()
        self.graph_canvas = FigureCanvasKivyAgg(figure=self.fig)
        self.graph_added = True
        self.symbols_graph.add_widget(self.graph_canvas)

    def update_minmax(self, values):
        min_val, max_val = np.min(values), np.max(values)
        if self.current_min is None or self.current_min > min_val:
            self.current_min = min_val
        if self.current_max is None or self.current_max < max_val:
            self.current_max = max_val
        val_range = self.current_max - self.current_min
        self.margin = 5 * val_range / 100

    def load_graphs(self, dt):
        if self.symbols_graph is None:
            Clock.schedule_interval(self.load_graphs, self.check_delay)
        to_fetch = [symbol for symbol in self.displayed_symbol.keys() if
                    self.displayed_symbol[symbol] and symbol not in self.symbols_lines]
        to_remove = [symbol for symbol in self.displayed_symbol.keys() if not self.displayed_symbol[symbol]]
        self.init_graph()
        for test_fetch in to_fetch:
            print('fetching', test_fetch)
            values = TwentyFourHrTickerEvent.find_valuesforsymbol(test_fetch)
            self.update_minmax(values)
            self.ax.plot(values)
            self.symbols_lines[test_fetch] = self.ax.lines[-1]
            print(self.symbols_lines[test_fetch])
        for test_remove in to_remove:
            print('removing', test_remove)
            if test_remove in self.symbols_lines:
                self.ax.lines.remove(self.symbols_lines[test_remove])
                del self.symbols_lines[test_remove]
        print(self.ax.lines)
        self.ax.set_ylim(self.current_min - self.margin, self.current_max + self.margin)
        self.graph_canvas.draw()

    def symbol_button_callback(self, instance: ToggleButton, state):
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
