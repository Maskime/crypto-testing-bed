from typing import Optional, Type, TypeVar, Dict

# "e": "24hrTicker",  // Event type
from mongoengine import Document, FloatField, IntField, StringField

T = TypeVar('T', bound='TwentyFourHrTickerEvent')


class TwentyFourHrTickerEvent(Document):
    symbol: StringField = StringField()

    price_change: FloatField = FloatField()
    price_change_percent: FloatField = FloatField()
    weighted_avg_price: FloatField = FloatField()
    previous_day_close_price: FloatField = FloatField()
    best_bid_price: FloatField = FloatField()
    best_bid_quantity: FloatField = FloatField()
    best_ask_price: FloatField = FloatField()
    best_ask_quantity: FloatField = FloatField()
    open_price: FloatField = FloatField()
    high_price: FloatField = FloatField()
    low_price: FloatField = FloatField()
    total_traded_base_asset_volume: FloatField = FloatField()
    total_traded_quote_asset_volume: FloatField = FloatField()
    event_time: IntField = IntField()
    close_trade_quantity: IntField = IntField()
    statistics_open_time: IntField = IntField()
    statistics_close_time: IntField = IntField()
    first_trade_id: IntField = IntField()
    last_trade_id: IntField = IntField()
    total_number_trades: IntField = IntField()

    fields_translation: Dict[str, str] = {
        'symblol': 's',
        # "p": "0.0015",      // Price change
        'price_change': 'p',
        # "P": "250.00",      // Price change percent
        'price_change_percent': 'P',
        # "w": "0.0018",      // Weighted average price
        'weighted_avg_price': 'w',
        # "x": "0.0009",      // Previous day's close price
        'previous_day_close_price': 'x',
        # "b": "0.0024",      // Best bid price
        'best_bid_price': 'b',
        # "B": "10",          // Best bid quantity
        'best_bid_quantity': 'B',
        # "a": "0.0026",      // Best ask price
        'best_ask_price': 'a',
        # "A": "100",         // Best ask quantity
        'best_ask_quantity': 'A',
        # "o": "0.0010",      // Open price
        'open_price': 'o',
        # "h": "0.0025",      // High price
        'high_price': 'h',
        # "l": "0.0010",      // Low price
        'low_price': 'l',
        # "v": "10000",       // Total traded base asset volume
        'total_traded_base_asset_volume': 'v',
        # "q": "18",          // Total traded quote asset volume
        'total_traded_quote_asset_volume': 'q',
        # "E": 123456789,     // Event time
        'event_time': 'E',
        # "Q": "10",          // Close trade's quantity
        'close_trade_quantity': 'Q',
        # "O": 0,             // Statistics open time
        'statistics_open_time': 'O',
        # "C": 86400000,      // Statistics close time
        'statistics_close_time': 'C',
        # "F": 0,             // First trade ID
        'first_trade_id': 'F',
        # "L": 18150,         // Last trade Id
        'last_trade_id': 'L',
        # "n": 18151          // Total number of trades
        'total_number_trades': 'n'
    }

    def __init__(self, *args, **values) -> None:
        super().__init__(*args, **values)

    @classmethod
    def object_hook(cls, remote_dict) -> Optional[T]:
        if 'e' not in remote_dict or remote_dict['e'] != '24hrTicker':
            return None
        out: TwentyFourHrTickerEvent = TwentyFourHrTickerEvent()
        out.symbol = remote_dict[out.fields_translation['symblol']]
        # Floats
        out.price_change = float(remote_dict[out.fields_translation['price_change']])
        out.price_change_percent = float(remote_dict[out.fields_translation['price_change_percent']])
        out.weighted_avg_price = float(remote_dict[out.fields_translation['weighted_avg_price']])
        out.previous_day_close_price = float(remote_dict[out.fields_translation['previous_day_close_price']])
        out.best_bid_price = float(remote_dict[out.fields_translation['best_bid_price']])
        out.best_bid_quantity = float(remote_dict[out.fields_translation['best_bid_quantity']])
        out.best_ask_price = float(remote_dict[out.fields_translation['best_ask_price']])
        out.best_ask_quantity = float(remote_dict[out.fields_translation['best_ask_quantity']])
        out.open_price = float(remote_dict[out.fields_translation['open_price']])
        out.high_price = float(remote_dict[out.fields_translation['high_price']])
        out.low_price = float(remote_dict[out.fields_translation['low_price']])
        out.total_traded_base_asset_volume = float(remote_dict[out.fields_translation['total_traded_base_asset_volume']])
        out.total_traded_quote_asset_volume = float(remote_dict[out.fields_translation['total_traded_quote_asset_volume']])
        out.close_trade_quantity = float(remote_dict[out.fields_translation['close_trade_quantity']])
        # Ints
        out.event_time = int(remote_dict[out.fields_translation['event_time']])
        out.statistics_open_time = int(remote_dict[out.fields_translation['statistics_open_time']])
        out.statistics_close_time = int(remote_dict[out.fields_translation['statistics_close_time']])
        out.first_trade_id = int(remote_dict[out.fields_translation['first_trade_id']])
        out.last_trade_id = int(remote_dict[out.fields_translation['last_trade_id']])
        out.total_number_trades = int(remote_dict[out.fields_translation['total_number_trades']])

        return out

    def __repr__(self):
        return str(self.__dict__)
