from binance.client import Client
from binance.websockets import BinanceSocketManager
from datetime import datetime 
import configparser
import json
import requests
import ccxt
import time
from pprint import pprint 

def table(values):
    first = values[0]
    keys = list(first.keys()) if isinstance(first, dict) else range(0, len(first))
    widths = [max([len(str(v[k])) for v in values]) for k in keys]
    string = ' | '.join(['{:<' + str(w) + '}' for w in widths])
    return "\n".join([string.format(*[str(v[k]) for k in keys]) for v in values])


config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['BINANCE']['API_KEY']
SECRET_KEY = config['BINANCE']['SECRET_KEY']
API_URL = config['BINANCE']['API_URL']


print('CCXT Version: ', ccxt.__version__)
exchange_id = 'binance'
exchange = ccxt.binance({
    'options': {
        'adjustForTimeDifference': True,
        'defaultType': 'future'
    },
    'enableRateLimit': True,
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
})



markets = exchange.load_markets()
# print(exchange_id, markets)
# print(list(markets.keys()))

# print(dir(exchange))

# print(exchange.fetchStatus())

# print(exchange.fetchTicker('BTC/USDT'))
# print(exchange.fetchBalance())

# check whether enough balance for futures margin trading
balance = exchange.fetch_balance()
pprint(balance)
# print(balance['total'])


# symbol = 'BTC/USDT'
symbol = 'OCEAN/USDT'
market = exchange.market(symbol)

# response = exchange.fetch_positions(id, symbol)
# pprint(response)


# pprint(market['id'])
# setting up leverage 
# exchange.fapiPrivate_post_leverage({  # https://github.com/ccxt/ccxt/wiki/Manual#implicit-api-methods
#     'symbol': market['id'],  # https://github.com/ccxt/ccxt/wiki/Manual#symbols-and-market-ids
#     'leverage': 5,  # target initial leverage, int from 1 to 125
# })

# # 
# # exchange.fapiPrivatePostMarginType ({
# exchange.fapiPrivate_post_margintype ({
#     'symbol': market['id'],
#     'marginType': 'ISOLATED', # or 'CROSSED'
# })

# exchange.verbose = True 
# print(market['info']['orderTypes'])

print('Getting all my positions:')
positions = exchange.fapiPrivateV2_get_positionrisk()
print(table(positions))
print('----------------------------------------------------------------------')
pprint(positions)

# getting all my positions of specific symbol on futures market
# positions = balance['info']['positions']  # https://github.com/ccxt/ccxt/wiki/Manual#balance-structure

positions_by_ids = exchange.index_by(positions, 'symbol')  # binance's symbol == ccxt's id
position = exchange.safe_value(positions_by_ids, market['id'])
pprint(position)
print('-----------------------------------------')

print('Your profit and loss for your', symbol, 'position is', position['unRealizedProfit'])
print('Your liquidation price for your', symbol, 'position is', position['liquidationPrice'])



# https://binance-docs.github.io/apidocs/futures/en/#change-position-mode-trade

print('Getting your current position mode (One-way or Hedge Mode):')
response = exchange.fapiPrivate_get_positionside_dual()
if response['dualSidePosition']:
    print('You are in Hedge Mode')
else:
    print('You are in One-way Mode')

print('----------------------------------------------------------------------')

orderbook = exchange.fetch_order_book(symbol)
print(orderbook['bids'])
print(type(orderbook['bids']))

bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
spread = (ask - bid) if (bid and ask) else None
print (exchange.id, ':', symbol,  'market price', { 'bid': bid, 'ask': ask, 'spread': spread })




# client = Client(api_key = API_KEY, api_secret = SECRET_KEY)
# bm = BinanceSocketManager(client, user_timeout=60)

# def handle_message(msg):
#     print(f'Time: {datetime.fromtimestamp(msg["k"]["t"]/1000)} - Symbol: {msg["k"]["s"]} - Close Price: {msg["k"]["c"]} - Volume: {msg["k"]["v"]}')


# # balance = client.get_asset_balance(asset='ETH')
# # f'balance = {balance}'

# conn_key = bm.start_kline_socket('BTCUSDT', handle_message)
# # conn_key = bm.start_symbol_ticker_futures_socket('BTCUSDT', handle_message)
# # conn_key = bm.start_symbol_ticker_futures_socket('ETHUSDT', handle_message)
# # conn_key = bm.start_symbol_ticker_futures_socket('ETHUSDT', handle_message)
# # conn_key = bm.start_symbol_ticker_futures_socket('ETHUSDT', handle_message)


# bm.start()

# time.sleep(10)

# bm.stop_socket(conn_key)
