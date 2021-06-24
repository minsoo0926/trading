import asyncio
from datetime import datetime, timedelta
import sys
import configparser
import websocket

# BINANCE_SYMBOL = 'btcusdt'
# COINBASE_SYMBOL = 'BTC-USD'
BINANCE_SUBSCRIBE = '{ "method": "SUBSCRIBE", "params": [ "btcusdt@kline_1M"], "id": 1 }'
COINBASE_SUBSCRIBE = '{ "type": "subscribe", "product_ids": ["BTC-USD"], "channels": [ "ticker"] }'

config = configparser.ConfigParser()
config.read('../config.ini')

# B_WSS = config['BINANCE']['WS_URL']
# C_WSS = config['COINBASE']['WS_URL']

from client import Client

B_WSS = 'wss://stream.binance.com:9443/ws'
websocket.enableTrace(True)
binance = Client(B_WSS, 'binance')
# copro = Coinbase(B_WSS, 'copro')

binance.start()
# copro.start()