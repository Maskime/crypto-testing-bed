mongo_params = {
    "alias": "default",
    "name": "crypto-test-bed",
    "db": "crypto-test-bed",
    "host": "localhost",
    "port": 27017,
    "username": "root",
    "password": "prout",
    "authentication_source": "admin",
    "authentication_mechanism": "SCRAM-SHA-1"
}

time_limits = {
    "close": 10,
    "parallel": 5
}

binance = {
    "base_url": 'wss://stream.binance.com:9443/ws/',
    'ticker_arr': '!ticker@arr',
    'enable_trace': True
}

markets = ['BTC', 'BNB', 'ETH', 'PAX', 'USDT', 'TUSD']
