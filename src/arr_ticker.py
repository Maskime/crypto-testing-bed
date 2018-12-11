import json
import sched
from threading import Thread
from typing import Dict
from typing import List

import websocket
from mongoengine import connect

import configuration as cfg
from documents.binance import TwentyFourHrTickerEvent


class TickerSave(Thread):
    connection_params = None
    ws_response: List[TwentyFourHrTickerEvent] = None

    def run(self):
        super().run()
        connect(**self.connection_params)
        print('[{}] Saving ticker response '.format(self.getName()), end='')
        for ticker in self.ws_response:
            ticker.save()
            print('.', end='')
        print('Done')


class ArrayTicker(Thread):
    events: Dict[int, List[sched.Event]] = {}

    current_websocket: websocket.WebSocketApp

    def run(self):
        super().run()
        self.createwsconnection()

    def on_message(self, *args):
        json_message = json.loads(args[0], object_hook=TwentyFourHrTickerEvent.object_hook)
        save_thread = TickerSave()
        save_thread.connection_params = cfg.mongo_params
        save_thread.ws_response = json_message
        save_thread.start()

    def on_error(self, *args):
        print('Error')
        print(args[0])

    def on_close(self, *args):
        print('On close', args)

    def on_open(self, *args):
        print('Connection opened')

    def createwsconnection(self):
        print('Creating a new WS connection')
        websocket.enableTrace(cfg.binance['enable_trace'])
        websocket_url = cfg.binance['base_url'] + cfg.binance['ticker_arr']
        self.current_websocket: websocket.WebSocketApp = websocket.WebSocketApp(websocket_url,
                                                                                on_message=self.on_message,
                                                                                on_error=self.on_error,
                                                                                on_close=self.on_close)
        self.current_websocket.on_open = self.on_open
        self.current_websocket.run_forever()
