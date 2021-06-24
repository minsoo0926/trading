from datetime import datetime, timezone
import pandas as pd 

import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots

from scipy.stats import zscore 
import numpy as np 

# import matplotlib.image as mpimg
# import matplotlib.pyplot as plt
# from IPython.display import Image

import configparser
import json
import requests
import ccxt
import time

from pprint import pprint 
from urllib.parse import urljoin 

config = configparser.ConfigParser()
config.read('../config.ini')


BINANCE_SYMBOL = 'BTC/USDT'
COPRO_SYMBOL = 'BTC/USD'

COPRO_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S' # format for general datetime params. 

# BINANCE_COLUMNS = ['time', 'open', 'high', 'low', 'close', 'volume']
# COPRO_COLUMNS  = ['time', 'low', 'high', 'open', 'close', 'volume']
COLUMNS  = ['datetime', 'open', 'high', 'low', 'close', 'volume']

BINANCE_API_KEY = config['BINANCE']['API_KEY']
BINANCE_SECRET_KEY = config['BINANCE']['SECRET_KEY']
BINANCE_API_URL = config['BINANCE']['API_URL']

COPRO_API_KEY = config['COINBASE']['API_KEY']
COPRO_SECRET_KEY = config['COINBASE']['SECRET_KEY']
COPRO_API_URL = config['COINBASE']['API_URL']

# HEIGHT = 1000
# WIDTH = 1500


def num_tick(timeframe):
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

    return(tick)



def ohlcv_df(symbol, exchange, timeframe, since=None):

    tick = num_tick(timeframe)

    data = []
    now_timestamp = exchange.milliseconds()
    since_timestamp = exchange.parse8601(since)

    print(f'Data fetching: from {exchange.iso8601(since_timestamp)} - to {exchange.iso8601(now_timestamp)}')

    if (since_timestamp == None or since_timestamp > now_timestamp):
        print('Fetching from: ', exchange.iso8601(since_timestamp))
        data = exchange.fetch_ohlcv(symbol, timeframe)
        print('Fetching finished')  
        return(data)

    while since_timestamp < now_timestamp: 
        print('Fetching from: ', exchange.iso8601(since_timestamp))
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
    


def dt_to_str(dt, format):
    return(dt.strftime(format))


def ts_to_dt(ts, tzinfo='korea'):     
    # ts_binance_size = 13

    # KST = datetime.timezone(datetime.timedelta(hours=9))
    if tzinfo == 'binance':
        return(datetime.utcfromtimestamp(float(ts)/1000)) 
    elif tzinfo == 'coinbase':
        return(datetime.utcfromtimestamp(float(ts)))
    elif tzinfo == 'korea':
        return(datetime.fromtimestamp(float(ts)))


def binance_ts_to_dt(time):
    return(datetime.utcfromtimestamp(float(time)/1000))

def group_mean(df, key):
    '''
    grouping df by key (i.e. month=M, day=D) and return mean
    df: input dataframe 
    key: key to group 
    return: means of each item grouped 
    '''

    return(df.groupby(pd.Grouper(level='datetime', freq=key)).mean())


# def subset_sum(df, offset):
#     '''
#     calculate subset sum starting from next position until offset

#     '''
#      return df_price['price_usd_close'].iloc[item.name+1: item.name+offset].mean() - item['price_usd_close']


def one_day_from_df(df, date):
    '''
    extract one day data from dataframe
    df: input dataframe
    date: date to extract (i.e. 2020-04-1)
    return: one day (date) data as dataframe
    '''
    return(df.loc[date])

def mean_within_window(df, col, offset1=1, offset2=30):
    '''
    calculate mean of window (current, current + offset) items from dataframe
    '''
    # result = [df[col].iloc[row+offset1: row+offset2].mean() - df[col].iloc[row] for row in range(len(df))]
    return([df[col].iloc[row+offset1: row+offset2].mean() - df[col].iloc[row] for row in range(len(df))])


def mean_within_window_new(df, offset1=1, offset2=10):
    '''
    calculate mean of window (current, current + offset) items from dataframe
    '''
    # result = [df[col].iloc[row+offset1: row+offset2].mean() - df[col].iloc[row] for row in range(len(df))]
    return([df.iloc[row+offset1: row+offset2].mean() - df.iloc[row] for row in range(len(df))])

# in_date: string type
# return: datetime format  from('%Y-%m-%d %H:%M:%S' ) ==> to('%Y%m%dT%H%M%S')
def time_format_conversion(in_date):
    d = datetime.strptime(in_date, '%Y-%m-%d %H:%M:%S')
    return(d.strftime('%Y%m%dT%H%M%S'))



# merge two dataframes into one for data feeding 
def merge_price_signal(price, signal):
    return(pd.merge(price, signal, left_index=True, right_index=True))


def print_trade_analysis(analyzer):
    '''
    Function to print the Technical Analysis results in a nice format.
    '''
    #Get the results we are interested in
    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total
    win_streak = analyzer.streak.won.longest
    lose_streak = analyzer.streak.lost.longest
    pnl_net = round(analyzer.pnl.net.total,2)
    strike_rate = (total_won / total_closed) * 100
    #Designate the rows
    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    h2 = ['Strike Rate','Win Streak', 'Losing Streak', 'PnL Net']
    r1 = [total_open, total_closed,total_won,total_lost]
    r2 = [strike_rate, win_streak, lose_streak, pnl_net]
    #Check which set of headers is the longest.
    if len(h1) > len(h2):
        header_length = len(h1)
    else:
        header_length = len(h2)
    #Print the rows
    print_list = [h1,r1,h2,r2]
    row_format ="{:<15}" * (header_length + 1)
    print("Trade Analysis Results:")
    for row in print_list:
        print(row_format.format('',*row))


def print_sqn(analyzer):
    sqn = round(analyzer.sqn,2)
    print('SQN: {}'.format(sqn))


def outliers_removal(df):
    z_scores = zscore(df)
    abs_z_scores = np.abs(z_scores)
    filtered_entries = (abs_z_scores < 3).all(axis=1)
    return(df[filtered_entries])

# remove first element and add last 
def shift_n_and_add_one(df, n, item):
    tmp_df = df.shift(-n)
    tmp_df[-1] = item
    return(tmp_df) 
    