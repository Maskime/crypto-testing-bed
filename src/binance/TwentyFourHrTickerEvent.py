from typing import Optional, Type, TypeVar

# "e": "24hrTicker",  // Event type
# "E": 123456789,     // Event time
# "s": "BNBBTC",      // Symbol
# "p": "0.0015",      // Price change
# "P": "250.00",      // Price change percent
# "w": "0.0018",      // Weighted average price
# "x": "0.0009",      // Previous day's close price
# "c": "0.0025",      // Current day's close price
# "Q": "10",          // Close trade's quantity
# "b": "0.0024",      // Best bid price
# "B": "10",          // Best bid quantity
# "a": "0.0026",      // Best ask price
# "A": "100",         // Best ask quantity
# "o": "0.0010",      // Open price
# "h": "0.0025",      // High price
# "l": "0.0010",      // Low price
# "v": "10000",       // Total traded base asset volume
# "q": "18",          // Total traded quote asset volume
# "O": 0,             // Statistics open time
# "C": 86400000,      // Statistics close time
# "F": 0,             // First trade ID
# "L": 18150,         // Last trade Id
# "n": 18151          // Total number of trades


T = TypeVar('T', bound='TwentyFourHrTickerEvent')


class TwentyFourHrTickerEvent(object):
    event_time: int = 0
    symbol: str = ''
    price_change: float = 0.0
    price_change_percent: float = 0.0
    weighted_avg_price: float = 0.0
    previous_day_close_price: float = 0.0
    close_trade_quantity: int = 0
    best_bid_price: float = 0.0
    best_bid_quantity: float = 0.0
    best_ask_price: float = 0.0
    best_ask_quantity: float = 0.0
    open_price: float = 0.0
    high_price: float = 0.0
    low_price: float = 0.0
    total_traded_base_asset_volume: float = 0.0
    total_traded_quote_asset_volume: float = 0.0
    statistics_open_time: int = 0
    statistics_close_time: int = 0.0
    first_trade_id: int = 0
    last_trade_id: int = 0
    total_number_trades: int = 0

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def object_hook(cls, dict) -> Optional[T]:
        if 'e' not in dict or dict['e'] != '24hrTicker':
            return None
        # print("Converting to objec :", dict)
        out: TwentyFourHrTickerEvent = TwentyFourHrTickerEvent()
        out.event_time = dict['E']
        return out

    def __repr__(self):
        return str(self.__dict__)