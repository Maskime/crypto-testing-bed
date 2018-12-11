import os

import kivy
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel

from gui.widgets import Exploration

kivy.require('1.10.1')


class CTBMain(TabbedPanel):
    Exploration
    pass


class CryptoTestBedApp(App):
    kv_directory = os.path.dirname(os.path.realpath(__file__))

    def build(self):
        self.title = 'Crypto Test Bed (CTB)'
        return CTBMain()
