import websocket
import json
from binance.TwentyFourHrTickerEvent import TwentyFourHrTickerEvent

try:
    import thread
except ImportError:
    import _thread as thread


def on_message(ws, message):
    print('message', datetim)
    json_message = json.loads(message,object_hook=TwentyFourHrTickerEvent.object_hook)
    # print(json_message)
    # print(json.dumps(json_message, sort_keys=False, indent=4))
    print("------------------------------------")


def on_error(ws, error):
    print(error)


def on_close(ws):
    print('Closed')


def on_open(ws):
    print('Open')


if __name__ == '__main__':
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/!ticker@arr",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()