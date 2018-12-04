from threading import Thread
from typing import List

from mongoengine import connect

from documents.TwentyFourHrTickerEvent import TwentyFourHrTickerEvent


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
