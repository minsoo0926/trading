from datetime import datetime 
import pandas as pd 

import ccxt
import time
from .date_utils import validate_dateformat

# BINANCE_SYMBOL = 'BTC/USDT'
# COPRO_SYMBOL = 'BTC/USD'

COLUMNS  = ['datetime', 'open', 'high', 'low', 'close', 'volume']


def num_of_ticks(timeframe):
    """
    returns number of ticks to count for a given timeframe  
    timeframe: 1m, 1h, 1d 
    """
    msec = 1000
    minute = 60 * msec 
    hour = 60 * minute
    day = 24 * hour  

    if timeframe == '1m': 
        tick = minute
    elif timeframe == '1h':
        tick = hour 
    elif timeframe == '1d':
        tick = day 
    
    return(tick)


def fetch_ohlcv(symbol, exchange, timeframe, start, end=None):
    """
    returns ohlcv data from specific date to now for a given symbol in an exchange 

    symbol: 'BTC/USDT', 'BTC/USD'
    exchange: ccxt exchange  
    timeframe: '1m', '1h', '1d'
    start, end: 'YYYY-MM-DD HH:MM:SS' format  
    returns ohlcv data as a python list 
    """ 

    tick = num_of_ticks(timeframe)
    data = []

    if (not validate_dateformat(start)):
        return {'status': 'error', 'message': 'param start is not a correct date format.'}

    if (end != None) and (not validate_dateformat(end)):
        return {'status': 'error', 'message': 'param end is not a correct date format.'}

    start_timestamp = exchange.parse8601(start)
    end_timestamp = exchange.milliseconds() if (end == None) else exchange.parse8601(end)

    if (start_timestamp >= end_timestamp):
        return {'status': 'error', 'message': 'param start cannot be later than param end.'}        

    while start_timestamp < end_timestamp: 
        print(f'Data fetching ({exchange.id}): from  {exchange.iso8601(start_timestamp)} - to {exchange.iso8601(end_timestamp)}')
        candles = exchange.fetch_ohlcv(symbol, timeframe, since=start_timestamp)
        start_timestamp = candles[-1][0] + tick 
        data += candles

    print('Fetching finished.')

    return({'status': 200, 'data': data})


def ohlcv_to_df(ohlcv_data):
    """
    transforms ohlcv data to python dataframe data
    """

    df = pd.DataFrame(ohlcv_data, columns=COLUMNS)
    df.datetime = pd.to_datetime(df.datetime, unit='ms')
    df.set_index('datetime', inplace=True)
    return(df)


# merge two dataframes into one for data feeding 
def merge_df(a_df, b_df):
    """
    merging two dataframes 
    """

    return(pd.merge(a_df, b_df, left_index=True, right_index=True))