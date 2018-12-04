import json
import sched
from threading import Thread

import time
from typing import Dict, List

import websocket
import configuration as cfg

from TickerSave import TickerSave
from documents.TwentyFourHrTickerEvent import TwentyFourHrTickerEvent


class ArrayTicker(Thread):
    schedule: sched.scheduler = sched.scheduler(time.time, time.sleep)
    scheduler_started = False

    events: Dict[int, List[sched.Event]] = {}

    def run(self):
        super().run()
        self.createwsconnection()

    def on_message(self, *args):
        print('[{}] Current scheduler state is {}, events len {}'.format(self.getName(), self.scheduler_started, len(self.schedule.queue)))
        json_message = json.loads(args[0], object_hook=TwentyFourHrTickerEvent.object_hook)
        save_thread = TickerSave()
        save_thread.connection_params = cfg.mongo_params
        save_thread.ws_response = json_message
        save_thread.start()

    def on_error(self, *args):
        print('Error')
        print(ws)
        self.cancelevents(ws)

    def on_close(self, *args):
        print('On close', args)
        # self.cancelevents(ws)

    def on_open(self, ws):
        self.createclosingevent(ws)

    def createclosingevent(self, ws: websocket.WebSocketApp):
        print('Creating closing events close {}, parallel {}'.format(cfg.time_limits['close'], cfg.time_limits['parallel']))
        closeevent = self.schedule.enter(cfg.time_limits['close'], 1, self.closews, kwargs={'ws': ws})
        parallelevent = self.schedule.enter(cfg.time_limits['parallel'], 1, self.createwsconnection)
        ArrayTicker.events[id(ws)] = [closeevent, parallelevent]
        if not ArrayTicker.scheduler_started:
            print('starting scheduler')
            self.schedule.run(False)
            self.scheduler_started = True

    def createwsconnection(self):
        print('Creating a new WS connection')
        websocket.enableTrace(cfg.binance['enable_trace'])
        websocket_url = cfg.binance['base_url'] + cfg.binance['ticker_arr']
        ws: websocket.WebSocketApp = websocket.WebSocketApp(websocket_url,
                                                            on_message=self.on_message,
                                                            on_error=self.on_error,
                                                            on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()
        self.createclosingevent(ws)

    def closews(self, ws: websocket.WebSocketApp):
        print('Closing ws connection id {}'.format(id(ws)))
        ws.close()

    def cancelevents(self, ws):
        currentid = id(ws)
        if currentid in ArrayTicker.events:
            print('Cancelling events', end=' ')
            for event in self.events[currentid]:
                self.schedule.cancel(event)
                print('.', end='')
            print(' Done.')
        else:
            print('Could not find the id {} in the list of the existing ws'.format(currentid))
