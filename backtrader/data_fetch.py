from datetime import datetime, timezone
import configparser
import json
import requests
import ccxt
import time
from pprint import pprint 
import pandas as pd
from urllib.parse import urljoin 
import utils 


config = configparser.ConfigParser()
config.read('../config.ini')


BINANCE_SYMBOL = 'BTC/USDT'
COPRO_SYMBOL = 'BTC/USD'

COPRO_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S' # format for general datetime params. 

BINANCE_COLUMNS = ['time', 'open', 'high', 'low', 'close', 'volume']
COPRO_COLUMNS  = ['time', 'low', 'high', 'open', 'close', 'volume']

BINANCE_API_KEY = config['BINANCE']['API_KEY']
BINANCE_SECRET_KEY = config['BINANCE']['SECRET_KEY']
BINANCE_API_URL = config['BINANCE']['API_URL']

COPRO_API_KEY = config['COINBASE']['API_KEY']
COPRO_SECRET_KEY = config['COINBASE']['SECRET_KEY']
COPRO_API_URL = config['COINBASE']['API_URL']

COLUMNS  = ['datetime', 'open', 'high', 'low', 'close', 'volume']



def ohlcv_df(symbol, exchange, timeframe, since=None):
    msec = 1000
    minute = 60 * msec
    hour = 60 *minute
    day = 24 * hour

    if timeframe == '1m':
        tick = minute
    elif timeframe == '1h':
        tick = hour
    elif timeframe == '1d':
        tick = day 

    data = []
    now_timestamp = exchange.milliseconds()
    since_timestamp = exchange.parse8601(since)

    print('Difference: ', (now_timestamp - since_timestamp)/minute, '(', exchange.iso8601(since_timestamp), '-', exchange.iso8601(now_timestamp), ')')

    if (since_timestamp == None or since_timestamp > now_timestamp):
        print('Fetching candles starting from: ', exchange.iso8601(since_timestamp))
        data = exchange.fetch_ohlcv(symbol, timeframe)
        print('Fetching finished')  
        return(data)


    while since_timestamp < now_timestamp: 
        print('Fetching candles starting from: ', exchange.iso8601(since_timestamp))
        candles = exchange.fetch_ohlcv(symbol, timeframe, since=since_timestamp)
        since_timestamp = candles[-1][0] + tick 
        data += candles

    print('Fetching finished')

    df = pd.DataFrame(data, columns=COLUMNS)
    df.datetime = pd.to_datetime(df.datetime, unit='ms')
    df.set_index('datetime', inplace=True)

    # df = pd.DataFrame(data, columns=COLUMNS).set_index('datetime')
    # df.index = pd.to_pydatetime(df.index, DEFAULT_DATETIME_FORMAT)
    return(df)


def ohlcv_print(exchange, data):
    return [(exchange.iso8601(ts), c) for ts, o, h, l, c, v in data]  
    

# ef merge_data_by_ts(d1, d2):

